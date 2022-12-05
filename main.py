import arcade
import ArcadeWindow
print("started arcade")

def main():
    print("running main")
    our_window = ArcadeWindow.GameWindow(1200, 800, "Arcade with a Window Class")
    our_window.setup()
    arcade.run()

    print("main successfully run")


main()