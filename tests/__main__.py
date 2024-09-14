import unittest

from .urls import default_urlpatterns, routify_urlpatterns


class DjangoRoutifyTests(unittest.TestCase):
    def test(self):
        # If default urlpatterns != routify urlpatterns test will be failed.
        for default_urls_obj, routify_urls_obj in zip(
            default_urlpatterns,
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
                # Checking if callbacks are the same is a bad idea,
                # because objects cannot be the same


if __name__ == '__main__':
    # Run test
    unittest.main()
