from main.settings import prod
if prod is False:
    from tests.test_utilities.passwordTest import TestPassword
    from tests.test_models.profileTest import ProfileTestCase
    from tests.test_utilities.tokenTest import TestToken
    from tests.test_views.index_test import IndexViewTestCase
    from tests.test_views.extract_details import ExtractEmailDetailsTestCase
    from tests.test_views.send_mail_test import SendMailTestCase
    from tests.test_views.login_test import LoginTestCase
    from tests.test_views.logout_test import LogoutTestCase
    from tests.test_views.confirm_pass_test import ConfirmPassTestCase
else:
    print("TestCases are not optimised for production")