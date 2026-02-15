from textnode import TextNode, TextType

def main():
    node = TextNode("Join the backend revolution", TextType.LINK, "https://www.boot.dev")
    print(node)


if __name__ == "__main__":
    main()
