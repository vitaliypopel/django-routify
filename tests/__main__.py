import unittest

from . import utils

from .trailing_slash_tests.urls import (
    default_with_trailing_urlpatterns,
    routify_with_trailing_urlpatterns,
    default_without_trailing_urlpatterns,
    routify_without_trailing_urlpatterns,
)

from .dynamic_url_patterns_tests.urls import (
    default_urlpatterns,
    default_based_urlpatterns,
    colon_based_urlpatterns,
    curly_based_urlpatterns,
    angle_based_urlpatterns,
)

from .single_method_decorators_tests.urls import (
    default_django_urlpatterns,
    routify_urlpatterns,
)


class TrailingSlashTests(unittest.TestCase):
    def test_urls_with_trailing_slash(self):
        # If default urlpatterns != routify urlpatterns test will be failed.
        for default_urls_obj, routify_urls_obj in zip(
            default_with_trailing_urlpatterns,
            routify_with_trailing_urlpatterns,
        ):
            for default_url, routify_url in zip(
                default_urls_obj.url_patterns,
                routify_urls_obj.url_patterns,
            ):
                self.assertEqual(
                    str(default_url.pattern),
                    str(routify_url.pattern),
                )
                self.assertEqual(
                    default_url.pattern.name,
                    routify_url.pattern.name,
                )
                # Checking if callbacks are the same is a bad idea,
                # because objects cannot be the same

    def test_urls_without_trailing_slash(self):
        for default_urls_obj, routify_urls_obj in zip(
                default_without_trailing_urlpatterns,
                routify_without_trailing_urlpatterns,
        ):
            for default_url, routify_url in zip(
                    default_urls_obj.url_patterns,
                    routify_urls_obj.url_patterns,
            ):
                self.assertEqual(
                    str(default_url.pattern),
                    str(routify_url.pattern),
                )
                self.assertEqual(
                    default_url.pattern.name,
                    routify_url.pattern.name,
                )
                # Checking if callbacks are the same is a bad idea,
                # because objects cannot be the same


class DynamicUrlPatternsTests(unittest.TestCase):
    def test_urls_with_dynamic_urls(self):
        # If urlpatterns with custom dynamic patterns are not the same test will be failed.
        for url_resolver in default_urlpatterns:

            for i in range(len(url_resolver.url_patterns)):
                default_pattern = default_urlpatterns[0].url_patterns[i].pattern
                default_based_pattern = default_based_urlpatterns[0].url_patterns[i].pattern
                colon_based_pattern = colon_based_urlpatterns[0].url_patterns[i].pattern
                curly_based_pattern = curly_based_urlpatterns[0].url_patterns[i].pattern
                angle_based_pattern = angle_based_urlpatterns[0].url_patterns[i].pattern

                self.assertTrue(all(
                    [
                        default_pattern,
                        default_based_pattern,
                        colon_based_pattern,
                        curly_based_pattern,
                        angle_based_pattern,
                    ]
                ))
                self.assertTrue(all(
                    [
                        default_pattern.name,
                        default_based_pattern.name,
                        colon_based_pattern.name,
                        curly_based_pattern.name,
                        angle_based_pattern.name,
                    ]
                ))


class SingleMethodDecoratorsTests(unittest.TestCase):
    def test_decorated_views(self):
        for default_urls_obj, routify_urls_obj in zip(
                default_django_urlpatterns,
                routify_urlpatterns,
        ):
            for default_url, routify_url in zip(
                    default_urls_obj.url_patterns,
                    routify_urls_obj.url_patterns,
            ):
                self.assertEqual(
                    str(default_url.pattern),
                    str(routify_url.pattern),
                )
                self.assertEqual(
                    default_url.pattern.name,
                    routify_url.pattern.name,
                )

                default_allowed_methods = utils.get_allowed_methods(default_url.callback) # get list of allowed methods
                routify_allowed_methods = utils.get_allowed_methods(routify_url.callback) # get list of allowed methods

                self.assertEqual(
                    default_allowed_methods,
                    routify_allowed_methods,
                )

if __name__ == '__main__':
    # Run test
    unittest.main()
