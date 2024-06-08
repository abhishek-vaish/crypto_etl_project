import logging
import sys

logger = logging.getLogger(name=__name__)
stdout = logging.StreamHandler(stream=sys.stdout)
fmt = logging.Formatter(fmt=
                        "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%("
                        "lineno)s | %(process)s >>> %(message)s "
                        )

stdout.setFormatter(fmt)
logger.addHandler(stdout)

logger.setLevel(logging.INFO)
