from context import Game


def is_valid_file():
    pass


def main():
    game = Game()

    while game.run():
        game = Game()

    game.quit()


if __name__ == '__main__':
    main()
