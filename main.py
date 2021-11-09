from gui.app import App


def main():
    app = App(manualControl=False, enableGhost=False, enablePwrPlt=False)
    app.run()


if __name__ == "__main__":
    main()
