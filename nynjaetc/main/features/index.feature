Feature: Index Page

Just some simple sanity checks on the index page of the application
This also serves as a good test that the lettuce and selenium
stuff is all hooked up properly and running.

    Scenario: Index Page Load
        Given I am not logged in
        When I access the url "/intro/"
        Then I see the header "nynjaetc"
        Then I see the sidebar

    Scenario: Index Page Load With Selenium
        Using selenium
        When I access the url "/intro/"
        Then I see the header "nynjaetc"
        Finished using selenium
