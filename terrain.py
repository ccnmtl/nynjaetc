# -*- coding: utf-8 -*-
from lettuce.django import django_url
from lettuce import before, after, world, step
from django.test import client
from django.test.utils import teardown_test_environment
from django.conf import settings
from django.contrib.auth.models import User
import sys
import os
import time

try:
    from lxml import html
    from selenium import webdriver
    #from selenium.webdriver.browser.browser_profile import browserProfile
    #from selenium.common.exceptions import NoSuchElementException
    #from selenium.webdriver.common.keys import Keys
    #import selenium
except:
    pass

def robust_string_compare(a, b):
    """ compare two strings but be a little flexible about it.

    try to handle case and whitespace variations without blowing up.
    this makes tests more robust in the face of template changes"""
    return a.strip().lower() == b.strip().lower()

def skip_selenium():
    return (os.environ.get('LETTUCE_SKIP_SELENIUM', False)
            or (hasattr(settings, 'LETTUCE_SKIP_SELENIUM')
            and settings.LETTUCE_SKIP_SELENIUM))


@before.harvest
def setup_browser(variables):
    world.using_selenium = False
    if skip_selenium():
        world.browser = None
        world.skipping = False
    else:
        browser = getattr(settings, 'BROWSER', 'Chrome')
        if browser == 'Chrome':
            world.browser = webdriver.Chrome()
        elif browser == 'Headless':
            world.browser = webdriver.PhantomJS()
        else:
            print "unknown browser: %s" % browser
            exit(1)
    world.client = client.Client()


@after.harvest
def teardown_browser(total):
    if not skip_selenium():
        world.browser.quit()


@before.harvest
def setup_database(_foo):
    # make sure we have a fresh test database
    os.system("rm -f lettuce.db")
    os.system("cp test_data/test.db lettuce.db")


@after.harvest
def teardown_database(_foo):
    os.system("rm -f lettuce.db")


@before.each_scenario
def clear_data(_foo):
    pass


@step(u'Using selenium')
def using_selenium(step):
    if skip_selenium():
        world.skipping = True
    else:
        world.using_selenium = True

@step(u'Finished using selenium')
def finished_selenium(step):
    if skip_selenium():
        world.skipping = False
    else:
        world.using_selenium = False

@before.each_scenario
def clear_selenium(step):
    world.using_selenium = False


@step(r'I access the url "(.*)"')
def access_url(step, url):
    if world.using_selenium:
        world.browser.get(django_url(url))
    else:
        
        response = world.client.get(django_url(url))
        if 'location' in response._headers:
            new_url = response._headers['location'][1]
            response = world.client.get(django_url(new_url))
        world.dom = html.fromstring(response.content)

@step(u'Then I click "([^"]*)"')
def then_i_click_group1(step, register):
    reg_btn = world.browser.find_element_by_link_text(register)
    reg_btn.click()
    

@step(u'Then I register a test user')
def then_i_register_a_test_user(step):
    form = world.browser.find_element_by_tag_name('form')
    username = world.browser.find_element_by_id('id_username')
    email = world.browser.find_element_by_id('id_email')
    pass1 = world.browser.find_element_by_id('id_password1')
    pass2 = world.browser.find_element_by_id('id_password2')
    username.send_keys('test')
    email.send_keys('t@t.com')
    pass1.send_keys('test')
    pass2.send_keys('test')
    form.submit()
    user = User.objects.get(username='test')
    user.is_active = True
    user.save()


@step(u'Given I am registered')
def given_i_am_registered(step):
    if User.objects.get(username='test'):
        assert True
    else:
        assert False, 'This step must be implemented'


@step(u'Then I verify that I am logged in')
def then_i_verify_that_i_am_logged_in(step):
    logged_in = world.browser.find_elements_by_class_name('navbar-text')
    assert logged_in[0].text == 'Logged in as test'


@step(u'I am not logged in')
def i_am_not_logged_in(step):
    if world.using_selenium:
        world.browser.get(django_url("/accounts/logout/"))
    else:
        world.client.logout()


@step(u'I am taken to a login screen')
def i_am_taken_to_a_login_screen(step):
    assert "Log in" in world.dom.cssselect('h2')[0].text


@step(u'there is not an? "([^"]*)" link')
def there_is_not_a_link(step, text):
    found = False
    for a in world.dom.cssselect("a"):
        if a.text and a.text.strip() == text:
            found = True
    assert not found


@step(u'there is an? "([^"]*)" link')
def there_is_a_link(step, text):
    found = False
    for a in world.dom.cssselect("a"):
        if a.text and a.text.strip() == text:
            found = True
    assert found


@step(u'I click the "([^"]*)" link')
def i_click_the_link(step, text):
    if not world.using_selenium:
        for a in world.dom.cssselect("a"):
            if a.text:
                if text.strip().lower() in a.text.strip().lower():
                    href = a.attrib['href']
                    response = world.client.get(django_url(href))
                    world.dom = html.fromstring(response.content)
                    return
        assert False, "could not find the '%s' link" % text
    else:
        try:
            link = world.browser.find_element_by_partial_link_text(text)
            assert link.is_displayed()
            link.click()
        except:
            try:
                time.sleep(1)
                link = world.browser.find_element_by_partial_link_text(text)
                assert link.is_displayed()
                link.click()
            except:
                world.browser.get_screenshot_as_file("/tmp/selenium.png")
                assert False, link.location


@step(u'I fill in "([^"]*)" in the "([^"]*)" form field')
def i_fill_in_the_form_field(step, value, field_name):
    # note: relies on input having id set, not just name
    if not world.using_selenium:
        assert False, "this step not implemented for the django test client"

    world.browser.find_element_by_id(field_name).send_keys(value)


@step(u'I submit the "([^"]*)" form')
def i_submit_the_form(step, elt_id):
    form = world.browser.find_element_by_id(elt_id)
    form.submit()
    if not world.using_selenium:
        assert False, "this step not implemented for the django test client"


@step('I go back')
def i_go_back(self):
    """ need to back out of games currently"""
    if not world.using_selenium:
        assert False, "this step not implemented for the django test client"
    world.browser.back()


@step(u'I wait for (\d+) seconds')
def wait(step, seconds):
    time.sleep(int(seconds))


@step(r'I see the header "(.*)"')
def see_header(step, text):
    if world.using_selenium:
        elt = world.browser.find_element_by_css_selector(".hero-unit>h1")
        assert text.strip() == elt.text.strip()
    else:
        header = world.dom.cssselect('h2')[0]
        assert text.strip() == header.text_content().strip()


@step(r'I see the sidebar')
def see_sidebar(self):
    if world.using_selenium:
        assert False, "this step needs to be implemented for selenium"
    else:
        assert len(world.dom.cssselect('#sidebar')) == 1


@step(r'I see the page title "(.*)"')
def see_title(step, text):
    if world.using_selenium:
        assert text == world.browser.title
    else:
        assert text == world.dom.find(".//title").text
