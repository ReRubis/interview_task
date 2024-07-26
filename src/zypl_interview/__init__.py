from src.zypl_interview.logger import setup_logging

package_name = __package__ or "zypl"


setup_logging(package_name)


del setup_logging, package_name
