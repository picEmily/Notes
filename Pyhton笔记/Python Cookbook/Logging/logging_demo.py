import logging
import logging.config


def main():

    logging.basicConfig(filename='app.log', level=logging.INFO)

    logging.error("test info")
    logging.debug("test info")
    logging.info("test info")


if __name__ == "__main__":
    main()
