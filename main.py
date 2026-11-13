
from drafter import *
from dataclasses import dataclass
import random


# WEBSITE INFORMATION

set_website_title("Baseball Card Collector")

set_site_information(
    author="James Gardella",
    description="Open virtual baseball card packs, collect players, and find rare cards.",
    sources="Classmates, LLM, Xavier Tan",
    planning="Copy of CS1 Final Project 1_ Design (1)(2).pdf",
    links=[
        "https://github.com/jamesgardella14/CISC106-Final-Project-"
    ]
)

set_website_style("dark")
hide_debug_information()
set_website_framed(False)


# DATACLASSES

@dataclass
class BaseballCard:
    player_name: str
    team: str
    year: int
    rarity: str
    position: str
    favorite: bool = False


@dataclass
class State:
    coins: int
    packs_opened: int
    collection: list[BaseballCard]
    current_pack: list[BaseballCard]
    selected_pack: str
    search_text: str
    favorites_only: bool


# BASEBALL PLAYER DATA

players = [
    ("Shohei Ohtani", "Dodgers", 2025, "DH"),
    ("Aaron Judge", "Yankees", 2025, "OF"),
    ("Mike Trout", "Angels", 2024, "OF"),
    ("Mookie Betts", "Dodgers", 2025, "OF"),
    ("Bryce Harper", "Phillies", 2025, "1B"),
    ("Ronald Acuna Jr.", "Braves", 2024, "OF"),
    ("Juan Soto", "Mets", 2025, "OF"),
    ("Freddie Freeman", "Dodgers", 2025, "1B"),
    ("Cal Raleigh", "Mariners", 2025, "C"),
    ("Paul Skenes", "Pirates", 2025, "P"),
    ("Bobby Witt Jr.", "Royals", 2025, "SS"),
    ("Gunnar Henderson", "Orioles", 2025, "SS"),
    ("Randy Johnson", "Diamondbacks", 2001, "P"),
    ("Derek Jeter", "Yankees", 2000, "SS"),
    ("Ken Griffey Jr.", "Mariners", 1997, "OF")
]


# PACK PRICES

def get_pack_price(pack_name: str) -> int:
    if pack_name == "Rookie Pack":
        return 50
    elif pack_name == "All-Star Pack":
        return 100
    else:
        return 150


# GENERATE A RANDOM CARD

def generate_card(pack_name: str) -> BaseballCard:
    player = random.choice(players)

    chance = random.randint(1, 100)

    if pack_name == "Legends Pack":
        if chance <= 10:
            rarity = "Legendary"
        elif chance <= 35:
            rarity = "Rare"
        elif chance <= 65:
            rarity = "Uncommon"
        else:
            rarity = "Common"

    elif pack_name == "All-Star Pack":
        if chance <= 4:
            rarity = "Legendary"
        elif chance <= 25:
            rarity = "Rare"
        elif chance <= 60:
            rarity = "Uncommon"
        else:
            rarity = "Common"

    else:
        if chance <= 2:
            rarity = "Legendary"
        elif chance <= 15:
            rarity = "Rare"
        elif chance <= 45:
            rarity = "Uncommon"
        else:
            rarity = "Common"

    return BaseballCard(
        player[0],
        player[1],
        player[2],
        rarity,
        player[3]
    )


# NAVIGATION

def navigation():
    return [
        "\n",
        Button("Home", "home"),
        Button("Pack Shop", "pack_shop"),
        Button("My Collection", "collection"),
        Button("Search Cards", "search_cards"),
        "\n"
    ]


# HOME PAGE

@route
def home(state: State) -> Page:
    content = [
        Header("BASEBALL CARD COLLECTOR"),
        "Welcome to Baseball Card Collector!",
        "\n",
        "Open virtual baseball card packs and build your collection.",
        "\n",
        Header("Your Account"),
        "Coins: " + str(state.coins),
        "Packs Opened: " + str(state.packs_opened),
        "Cards Collected: " + str(len(state.collection)),
        "\n",
        Button("Visit Pack Shop", "pack_shop"),
        Button("View My Collection", "collection")
    ]

    content += navigation()

    return Page(state, content)


# PACK SHOP PAGE

@route
def pack_shop(state: State) -> Page:
    content = [
        Header("PACK SHOP"),
        "Choose a pack to open.",
        "\n",
        "Rookie Pack - 50 coins",
        "All-Star Pack - 100 coins",
        "Legends Pack - 150 coins",
        "\n",
        "Your coins: " + str(state.coins),
        "\n",
        "Select a pack:",
        SelectBox(
            "pack_choice",
            ["Rookie Pack", "All-Star Pack", "Legends Pack"],
            state.selected_pack
        ),
        Button("Select Pack", "select_pack")
    ]

    content += navigation()

    return Page(state, content)


# SELECT PACK ROUTE

@route
def select_pack(state: State, pack_choice: str) -> Page:
    state.selected_pack = pack_choice

    price = get_pack_price(pack_choice)

    content = [
        Header("PACK SELECTED"),
        "You selected the " + pack_choice + ".",
        "Price: " + str(price) + " coins",
        "Your coins: " + str(state.coins),
        "\n"
    ]

    if state.coins >= price:
        content.append("You have enough coins to open this pack.")
        content.append(Button("Open Pack", "open_pack"))
    else:
        content.append("You do not have enough coins for this pack.")

    content.append(Button("Back to Shop", "pack_shop"))

    content += navigation()

    return Page(state, content)


# OPEN PACK ROUTE

@route
def open_pack(state: State) -> Page:
    price = get_pack_price(state.selected_pack)

    content = [
        Header("YOUR NEW PACK"),
        "\n"
    ]

    if state.coins < price:
        content.append("You do not have enough coins to open this pack.")
        content.append(Button("Back to Shop", "pack_shop"))

    else:
        state.coins = state.coins - price
        state.packs_opened += 1
        state.current_pack = []

        for i in range(5):
            card = generate_card(state.selected_pack)

            state.current_pack.append(card)
            state.collection.append(card)

        content.append("You opened a " + state.selected_pack + "!")
        content.append("Here are your five new cards:")
        content.append("\n")

        for card in state.current_pack:
            card_text = (
                card.player_name + " - " +
                card.team + " - " +
                str(card.year) + " - " +
                card.position + " - " +
                card.rarity
            )

            content.append(card_text)

            if card.rarity == "Legendary":
                content.append("LEGENDARY CARD! Great pull!")

            elif card.rarity == "Rare":
                content.append("You found a rare card!")

            content.append("\n")

        content.append("Coins remaining: " + str(state.coins))
        content.append(Button("Open Another Pack", "pack_shop"))
        content.append(Button("View Collection", "collection"))

    content += navigation()

    return Page(state, content)


# COLLECTION PAGE

@route
def collection(state: State, favorites_only: bool = False) -> Page:
    state.favorites_only = favorites_only

    content = [
        Header("MY COLLECTION"),
        "Total cards: " + str(len(state.collection)),
        "\n",
        "Show favorites only: ",
        CheckBox("favorites_only", state.favorites_only),
        Button("Apply Filter", "collection"),
        "\n"
    ]

    found_card = False

    for i in range(len(state.collection)):
        card = state.collection[i]

        if not state.favorites_only or card.favorite:
            found_card = True

            content.append(
                card.player_name + " - " +
                card.team + " - " +
                card.rarity
            )

            content.append(
                Button(
                    "View Card",
                    "card_details",
                    [Argument("card_index", i)]
                )
            )

            content.append("\n")

    if not found_card:
        content.append("No cards found.")

    content += navigation()

    return Page(state, content)


# CARD DETAILS PAGE

@route
def card_details(state: State, card_index: int) -> Page:
    content = [Header("CARD DETAILS")]

    if card_index < 0 or card_index >= len(state.collection):
        content.append("Card not found.")

    else:
        card = state.collection[card_index]

        content.append("Player: " + card.player_name)
        content.append("Team: " + card.team)
        content.append("Year: " + str(card.year))
        content.append("Position: " + card.position)
        content.append("Rarity: " + card.rarity)

        if card.favorite:
            content.append("This card is in your favorites.")
            content.append(
                Button(
                    "Remove from Favorites",
                    "toggle_favorite",
                    [Argument("card_index", card_index)]
                )
            )
        else:
            content.append("This card is not in your favorites.")
            content.append(
                Button(
                    "Add to Favorites",
                    "toggle_favorite",
                    [Argument("card_index", card_index)]
                )
            )

    content.append(Button("Back to Collection", "collection"))

    content += navigation()

    return Page(state, content)


# FAVORITE CARD ROUTE

@route
def toggle_favorite(state: State, card_index: int) -> Page:
    if 0 <= card_index < len(state.collection):
        card = state.collection[card_index]
        card.favorite = not card.favorite

    return card_details(state, card_index)


# SEARCH CARDS PAGE

@route
def search_cards(
    state: State,
    player_search: str = "",
    favorites_only: bool = False
) -> Page:

    state.search_text = player_search
    state.favorites_only = favorites_only

    content = [
        Header("SEARCH CARDS"),
        "Enter a player's name:",
        TextBox("player_search", state.search_text),
        "\n",
        "Search favorites only: ",
        CheckBox("favorites_only", state.favorites_only),
        "\n",
        Button("Search", "search_cards"),
        "\n",
        Header("Search Results")
    ]

    found_card = False

    for i in range(len(state.collection)):
        card = state.collection[i]

        name_matches = (
            player_search.lower() in card.player_name.lower()
        )

        favorite_matches = (
            not favorites_only or card.favorite
        )

        if name_matches and favorite_matches:
            found_card = True

            content.append(
                card.player_name + " - " +
                card.team + " - " +
                card.rarity
            )

            content.append(
                Button(
                    "View Card",
                    "card_details",
                    [Argument("card_index", i)]
                )
            )

            content.append("\n")

    if not found_card:
        content.append("No matching cards found.")

    content += navigation()

    return Page(state, content)


# START THE WEBSITE

start_server(
    State(
        coins=500,
        packs_opened=0,
        collection=[],
        current_pack=[],
        selected_pack="Rookie Pack",
        search_text="",
        favorites_only=False
    )
)
