import time
from seleniumbase import BaseCase

# Use SeleniumBase encryption for password obfuscation
from seleniumbase import encryption  # (CMD) "sbase encrypt"
password = encryption.decrypt("$^*ENCRYPT=HRpEfiEESjE=?&#$")


class TestSailsApp(BaseCase):

    def test_sails_app_landing_pages(self):
        # Go to the Sails app and verify the landing pages
        self.open("http://localhost:1337")
        self.assert_element("a.navbar-brand img.logo")
        self.assert_element('img[purpose="ship"]')
        self.click('[purpose="about-section"] a[href="/faq"]')
        self.assert_text("FAQ", "h1")
        self.click('footer a[href="/contact"]')
        self.assert_text("Get in touch", "h1")
        self.assert_element('button span:contains("Send message")')
        self.click('footer a[href="/legal/terms"]')
        self.assert_text("Terms of service", "h1")
        self.click('footer a[href="/legal/privacy"]')
        self.assert_text("privacy policy", "h1")
        self.assert_text("General information", "h3")
        self.click("header img.logo")
        self.assert_text("A new Sails app.", '[purpose="full-page-hero"] h1')
        self.click('div[purpose="more-info-text"] div:contains("Dive in")')
        self.assert_element('div[purpose="scroll-destination"] h3')
        self.assert_text("Let's get to work.", 'div[purpose="pep-talk"] h3')

    def test_sails_app_with_admin_user(self):
        # Login with the Admin User and verify
        self.open("http://localhost:1337")
        self.click('a[href="/login"]')
        email = "admin@example.com"
        self.type('input[type="email"]', email)
        self.type('input[type="password"]', password)
        self.click('button[type="submit"]')
        self.assert_text("Welcome!", "h1")
        self.assert_text("Account", "#header-account-menu-link")

        # Explore the "Update me email" page
        self.click('a:contains("Update my email")')
        self.assert_text("Update personal info", "h1")
        self.assert_element("input#full-name")
        self.assert_element("input#email-address")

        # Explore the "My account" page
        self.click('a:contains("Cancel")')
        self.assert_text("My account", "h1")
        self.assert_element('a:contains("Edit profile")')
        self.assert_element('a:contains("Change password")')

        # Explore a page that only logged-in users can access
        self.click("a.navbar-brand img.logo")
        self.click('button:contains("Open a modal")')
        self.assert_element("div.modal-header")
        self.click('button[data-dismiss="modal"]')

        # Logout and verify
        self.click("#header-account-menu-link")
        self.click('header a:contains("Sign out")')
        self.assert_element("#login div.container-fluid")
        self.assert_text("Sign in to your account", "h1")

    def test_sails_app_with_new_user(self):
        # Create a new user and find the welcome page
        self.open("http://localhost:1337")
        self.click('a:contains("Sign up")')
        name = "Johnny Lawrence"
        self.type("#full-name", name)
        timestamp = str(int(time.time()))
        email = "sensei+%s@example.com" % timestamp
        self.type("#email-address", email)
        self.type("#password", password)
        self.type("#confirm-password", password)
        self.click("#terms-agreement")
        self.click('button[type="submit"]')
        self.assert_text("Welcome!", "h1")

        # Verify new user infomation
        self.click("#header-account-menu-link")
        self.click('a:contains("Settings")')
        self.assert_text(name, "#account-overview div.container")
        self.assert_text(email, "#account-overview div.container")

        # Logout and verify
        self.click("#header-account-menu-link")
        self.click('header a:contains("Sign out")')
        self.assert_element("#login div.container-fluid")
        self.assert_text("Sign in to your account", "h1")

        # Login with the new user and verify
        self.type('input[type="email"]', email)
        self.type('input[type="password"]', password)
        self.click('button[type="submit"]')
        self.assert_text("Welcome!", "h1")

        # Re-verify new user infomation
        self.click("#header-account-menu-link")
        self.click('a:contains("Settings")')
        self.assert_text(name, "#account-overview div.container")
        self.assert_text(email, "#account-overview div.container")

        # Logout again and verify
        self.click("#header-account-menu-link")
        self.click('header a:contains("Sign out")')
        self.assert_element("#login div.container-fluid")
        self.assert_text("Sign in to your account", "h1")
