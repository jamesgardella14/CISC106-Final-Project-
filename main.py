
from drafter import *
from dataclasses import dataclass
import random


# Makes the website look like a baseball card shop
set_website_title("Baseball Card Collector")

add_website_css("""
body {
    background-color: #eef2f7;
    font-family: Arial, sans-serif;
}

h1, h2, h3 {
    color: #142d50;
}

button {
    background-color: #142d50;
    color: white;
    border-radius: 8px;
    padding: 10px 16px;
    margin: 5px;
    font-weight: bold;
}

button:hover {
    background-color: #315b89;
}

input, select {
    padding: 8px;
    border-radius: 5px;
}

hr {
    border: 1px solid #cbd5e1;
}
""")


# Stores information about each baseball card
@dataclass
class BaseballCard:
    player_name: str
    team: str
    year: int
    rarity: str
    position: str
    favorite: bool = False


# Stores information about the user and their game
@dataclass
class State:
    coins: int
    packs_opened: int
    collection: list[BaseballCard]
    current_pack: list[BaseballCard]
    selected_pack: str


# Creates a random baseball card
def generate_card(pack_name: str) -> BaseballCard:

    number = random.randint(1, 100)

    if pack_name == "Legends Pack":
        if number <= 35:
            rarity = "Common"
        elif number <= 65:
            rarity = "Uncommon"
        elif number <= 90:
            rarity = "Rare"
        else:
            rarity = "Legendary"

    else:
        if number <= 60:
            rarity = "Common"
        elif number <= 85:
            rarity = "Uncommon"
        elif number <= 97:
            rarity = "Rare"
        else:
            rarity = "Legendary"

    players = [
        ("Mike Trout", "Angels", 2024, "CF"),
        ("Aaron Judge", "Yankees", 2024, "RF"),
        ("Mookie Betts", "Dodgers", 2024, "RF"),
        ("Shohei Ohtani", "Dodgers", 2024, "DH"),
        ("Ronald Acuna Jr.", "Braves", 2024, "RF"),
        ("Bryce Harper", "Phillies", 2024, "1B"),
        ("Freddie Freeman", "Dodgers", 2024, "1B"),
        ("Juan Soto", "Mets", 2025, "RF"),
        ("Gunnar Henderson", "Orioles", 2024, "SS"),
        ("Bobby Witt Jr.", "Royals", 2024, "SS"),
        ("Cal Raleigh", "Mariners", 2025, "C"),
        ("Paul Skenes", "Pirates", 2025, "P")
    ]

    player = random.choice(players)

    return BaseballCard(
        player[0],
        player[1],
        player[2],
        rarity,
        player[3]
    )


# Gets the price of each pack
def get_pack_price(pack_name: str) -> int:

    if pack_name == "Rookie Pack":
        return 50

    elif pack_name == "All-Star Pack":
        return 100

    else:
        return 150


# Creates the navigation buttons used on the pages
def navigation():
    return [
        Button("HOME", "index"),
        Button("PACK SHOP", "pack_shop"),
        Button("MY COLLECTION", "collection"),
        Button("SEARCH", "search_cards"),
        "\n",
        HorizontalRule()
    ]


# MAIN HOME PAGE
@route
def index(state: State) -> Page:

    return Page(state, [
        Header("⚾ BASEBALL CARD COLLECTOR"),
        "OPEN PACKS  |  COLLECT PLAYERS  |  FIND LEGENDS",
        HorizontalRule(),

        Header("Your Account"),
        "Coins: " + str(state.coins),
        "Packs Opened: " + str(state.packs_opened),
        "Cards Collected: " + str(len(state.collection)),

        HorizontalRule(),

        Header("Welcome, Collector!"),
        "Build your collection by opening virtual baseball card packs.",
        "Each pack contains five random players.",
        "Try to find Common, Uncommon, Rare, and Legendary cards!",

        Header("Explore the Website"),
        Button("VISIT PACK SHOP", "pack_shop"),
        Button("OPEN A PACK", "select_pack"),
        Button("VIEW MY COLLECTION", "collection"),
        Button("SEARCH PLAYERS", "search_cards"),

        HorizontalRule(),
        "Good luck finding your favorite players!"
    ])


# PACK SHOP PAGE
@route
def pack_shop(state: State) -> Page:

    return Page(state, navigation() + [
        Header("THE PACK SHOP"),
        "Choose a pack and see what players you can collect.",

        HorizontalRule(),

        Header("Rookie Pack"),
        "Price: 50 Coins",
        "A basic pack containing five random cards.",

        Header("All-Star Pack"),
        "Price: 100 Coins",
        "A pack with five random cards and a chance at rare players.",

        Header("Legends Pack"),
        "Price: 150 Coins",
        "A special pack with a better chance of finding rare cards.",

        HorizontalRule(),

        "Your Coins: " + str(state.coins),
        Button("CHOOSE A PACK", "select_pack"),
        Button("BACK HOME", "index")
    ])


# SELECT PACK PAGE
@route
def select_pack(state: State) -> Page:

    return Page(state, navigation() + [
        Header("SELECT YOUR PACK"),
        "Choose which pack you want to open.",
        "You currently have " + str(state.coins) + " coins.",

        SelectBox(
            "pack_choice",
            ["Rookie Pack", "All-Star Pack", "Legends Pack"],
            state.selected_pack
        ),

        Button("OPEN SELECTED PACK", "open_pack"),
        Button("BACK TO SHOP", "pack_shop")
    ])


# OPENS THE PACK AND GENERATES FIVE CARDS
@route
def open_pack(state: State, pack_choice: str) -> Page:

    price = get_pack_price(pack_choice)

    state.selected_pack = pack_choice

    # Checks if the user has enough coins
    if state.coins < price:
        return Page(state, navigation() + [
            Header("NOT ENOUGH COINS"),
            "You need " + str(price) + " coins to open this pack.",
            "You currently have " + str(state.coins) + " coins.",
            Button("BACK TO SHOP", "pack_shop")
        ])

    # Takes coins and updates the pack count
    state.coins = state.coins - price
    state.packs_opened = state.packs_opened + 1

    state.current_pack = []

    # Generates five random cards
    for i in range(5):
        card = generate_card(pack_choice)

        state.current_pack.append(card)
        state.collection.append(card)

    # Displays the cards that were opened
    content = navigation() + [
        Header("YOU OPENED A " + pack_choice.upper() + "!"),
        "Here are your five new cards:",
        HorizontalRule()
    ]

    for card in state.current_pack:

        content.append(Header(card.player_name))
        content.append("Team: " + card.team)
        content.append("Year: " + str(card.year))
        content.append("Position: " + card.position)
        content.append("Rarity: " + card.rarity)

        if card.rarity == "Legendary":
            content.append("⭐ LEGENDARY PULL!")

        elif card.rarity == "Rare":
            content.append("🔥 RARE CARD!")

        content.append(HorizontalRule())

    content.append("Coins Remaining: " + str(state.coins))
    content.append(Button("VIEW COLLECTION", "collection"))
    content.append(Button("OPEN ANOTHER PACK", "select_pack"))

    return Page(state, content)


# COLLECTION PAGE
@route
def collection(state: State, favorites_only: bool = False) -> Page:

    content = navigation() + [
        Header("MY BASEBALL CARD COLLECTION"),
        "Total Cards: " + str(len(state.collection)),
        "Check the box to show only your favorite cards.",

        CheckBox("favorites_only", favorites_only),
        Button("APPLY FILTER", "collection"),

        HorizontalRule()
    ]

    found = False

    # Goes through every card in the collection
    for i in range(len(state.collection)):

        card = state.collection[i]

        if not favorites_only or card.favorite:

            found = True

            content.append(Header(card.player_name))
            content.append(card.team + " | " + str(card.year))
            content.append("Rarity: " + card.rarity)

            if card.favorite:
                content.append("⭐ FAVORITE")

            content.append(
                Button(
                    "VIEW CARD DETAILS",
                    "card_details",
                    [Argument("card_index", i)]
                )
            )

            content.append(HorizontalRule())

    if not found:
        content.append("No cards found. Open a pack to get started!")

    content.append(Button("OPEN ANOTHER PACK", "select_pack"))

    return Page(state, content)


# CARD DETAILS PAGE
@route
def card_details(state: State, card_index: int) -> Page:

    if card_index < 0 or card_index >= len(state.collection):
        return Page(state, [
            Header("Card not found."),
            Button("BACK TO COLLECTION", "collection")
        ])

    card = state.collection[card_index]

    return Page(state, navigation() + [
        Header("BASEBALL CARD DETAILS"),

        Header(card.player_name),
        "Team: " + card.team,
        "Year: " + str(card.year),
        "Position: " + card.position,
        "Rarity: " + card.rarity,

        HorizontalRule(),

        "Favorite Card:",
        CheckBox("favorite_choice", card.favorite),

        Button(
            "SAVE FAVORITE SETTING",
            "save_favorite",
            [Argument("card_index", card_index)]
        ),

        Button("BACK TO COLLECTION", "collection")
    ])


# SAVES WHETHER A CARD IS A FAVORITE
@route
def save_favorite(
    state: State,
    card_index: int,
    favorite_choice: bool
) -> Page:

    if 0 <= card_index < len(state.collection):
        state.collection[card_index].favorite = favorite_choice

    return card_details(state, card_index)


# PLAYER SEARCH PAGE
@route
def search_cards(state: State, player_search: str = "") -> Page:

    content = navigation() + [
        Header("SEARCH PLAYERS"),
        "Enter a player's name to search your collection.",

        TextBox("player_search"),
        Button("SEARCH", "search_cards"),

        HorizontalRule()
    ]

    if player_search != "":

        found = False

        # Searches through every card in the collection
        for i in range(len(state.collection)):

            card = state.collection[i]

            if player_search.lower() in card.player_name.lower():

                found = True

                content.append(Header(card.player_name))
                content.append("Team: " + card.team)
                content.append("Year: " + str(card.year))
                content.append("Rarity: " + card.rarity)

                content.append(
                    Button(
                        "VIEW CARD DETAILS",
                        "card_details",
                        [Argument("card_index", i)]
                    )
                )

                content.append(HorizontalRule())

        if not found:
            content.append("No matching players were found in your collection.")

    content.append(Button("BACK TO COLLECTION", "collection"))

    return Page(state, content)


# STARTS THE WEBSITE
start_server(
    State(
        coins=500,
        packs_opened=0,
        collection=[],
        current_pack=[],
        selected_pack="Rookie Pack"
    )
)
