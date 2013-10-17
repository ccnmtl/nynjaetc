Feature: Login 

Just some simple sanity checks on the index page of the application
This also serves as a good test that the lettuce and selenium
stuff is all hooked up properly and running.

    Scenario: Access login screen.
        Given I am not logged in
        When I access the url "/accounts/login/"
        Then I see the header "Log in"
        

    Scenario: Index Page Load
        Given I am not logged in
        When I access the url "/intro/"
        Then I see the header "Log in"

    Scenario: Index Page Load With Selenium
        Using selenium
        When I access the url "/accounts/login/"
        Then I click "Register"
        Then I register a test user

    Scenario: Index Page Load With Selenium
        Using selenium
        Given I am registered
        When I access the url "/accounts/login/"
        Then I fill in "test" in the "id_username" form field
        Then I fill in "test" in the "id_password" form field
        Then I submit the "application-login-form" form
        Then I verify that I am logged in
        Finished using selenium
