
from drafter import *
from dataclasses import dataclass
import random


set_website_title("Baseball Card Collector")

set_site_information(
    author="James Gardella",
    description="Open virtual baseball card packs, collect players, and find rare cards.",
    sources="Classmates, LLM, Xavier Tan",
    planning="Copy of CS1 Final Project 1_ Design (1).pdf",
    links=[
        "https://github.com/jamesgardella14/CISC106-Final-Project-"
    ]
)

set_website_style("default")
set_website_framed(False)
hide_debug_information()


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
    ("Ken Griffey Jr.", "Mariners", 1997, "OF"),
    ("David Ortiz", "Red Sox", 2007, "DH"),
    ("Ichiro Suzuki", "Mariners", 2004, "OF"),
    ("Albert Pujols", "Cardinals", 2009, "1B"),
    ("Cal Ripken Jr.", "Orioles", 1995, "SS"),
    ("Pedro Martinez", "Red Sox", 1999, "P"),
    ("Nolan Ryan", "Rangers", 1991, "P"),
    ("Tony Gwynn", "Padres", 1994, "OF"),
    ("Barry Bonds", "Giants", 2002, "OF"),
    ("Greg Maddux", "Braves", 1995, "P"),
    ("Mariano Rivera", "Yankees", 2003, "P")
]


def get_pack_price(pack_name: str) -> int:
    if pack_name == "Rookie Pack":
        return 50
    elif pack_name == "All-Star Pack":
        return 100
    elif pack_name == "Legends Pack":
        return 150
    else:
        return 50


def get_pack_size(pack_name: str) -> int:
    return 5


def get_pack_description(pack_name: str) -> str:
    if pack_name == "Rookie Pack":
        return "A basic pack with a chance to find rare players."
    elif pack_name == "All-Star Pack":
        return "A better pack with improved odds of rare cards."
    elif pack_name == "Legends Pack":
        return "The most expensive pack with the best rarity odds."
    else:
        return "Choose a pack to get started."


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

    new_card = BaseballCard(
        player[0],
        player[1],
        player[2],
        rarity,
        player[3]
    )

    return new_card


def card_description(card: BaseballCard) -> str:
    description = (
        card.player_name
        + " | "
        + card.team
        + " | "
        + str(card.year)
        + " | "
        + card.position
        + " | "
        + card.rarity
    )

    return description


def rarity_message(card: BaseballCard) -> str:
    if card.rarity == "Legendary":
        return "LEGENDARY PULL! An amazing card!"
    elif card.rarity == "Rare":
        return "RARE CARD! Great find!"
    elif card.rarity == "Uncommon":
        return "You found an uncommon card."
    else:
        return "You found a common card."


def count_favorites(cards: list[BaseballCard]) -> int:
    count = 0

    for card in cards:
        if card.favorite:
            count += 1

    return count


def count_rare_cards(cards: list[BaseballCard]) -> int:
    count = 0

    for card in cards:
        if card.rarity == "Rare" or card.rarity == "Legendary":
            count += 1

    return count


def navigation():
    return [
        "\n",
        HorizontalRule(),
        Button("Home", "home"),
        Button("Pack Shop", "pack_shop"),
        Button("My Collection", "collection"),
        Button("Search Cards", "search_cards"),
        "\n"
    ]


@route
def home(state: State) -> Page:
    content = [
        Header("BASEBALL CARD COLLECTOR"),
        "Welcome to Baseball Card Collector!",
        "\n",
        "Open virtual packs and build your baseball card collection.",
        "\n",
        Header("YOUR ACCOUNT"),
        "Coins: " + str(state.coins),
        "Packs Opened: " + str(state.packs_opened),
        "Cards Collected: " + str(len(state.collection)),
        "Favorite Cards: " + str(count_favorites(state.collection)),
        "Rare Cards: " + str(count_rare_cards(state.collection)),
        "\n",
        Header("GET STARTED"),
        "Visit the pack shop to purchase your first pack.",
        Button("Visit Pack Shop", "pack_shop"),
        Button("View My Collection", "collection"),
        "\n",
        "Your starting balance is 500 coins."
    ]

    content += navigation()

    return Page(state, content)


@route
def pack_shop(state: State) -> Page:
    content = [
        Header("PACK SHOP"),
        "Choose a pack to open.",
        "\n",
        Header("ROOKIE PACK"),
        "Price: 50 coins",
        get_pack_description("Rookie Pack"),
        "\n",
        Header("ALL-STAR PACK"),
        "Price: 100 coins",
        get_pack_description("All-Star Pack"),
        "\n",
        Header("LEGENDS PACK"),
        "Price: 150 coins",
        get_pack_description("Legends Pack"),
        "\n",
        "Your current balance: " + str(state.coins),
        "\n",
        "Select your pack:",
        SelectBox(
            "pack_choice",
            ["Rookie Pack", "All-Star Pack", "Legends Pack"],
            state.selected_pack
        ),
        Button("Choose Pack", "select_pack")
    ]

    content += navigation()

    return Page(state, content)


@route
def select_pack(state: State, pack_choice: str = "Rookie Pack") -> Page:
    valid_packs = [
        "Rookie Pack",
        "All-Star Pack",
        "Legends Pack"
    ]

    if pack_choice not in valid_packs:
        pack_choice = "Rookie Pack"

    state.selected_pack = pack_choice

    price = get_pack_price(pack_choice)

    content = [
        Header("PACK SELECTED"),
        "You selected the " + pack_choice + ".",
        "\n",
        "Price: " + str(price) + " coins",
        "Your balance: " + str(state.coins),
        "\n",
        get_pack_description(pack_choice),
        "\n"
    ]

    if state.coins >= price:
        content.append("You have enough coins to open this pack.")
        content.append(Button("Open My Pack", "open_pack"))
    else:
        content.append("You do not have enough coins.")
        content.append(Button("Return to Pack Shop", "pack_shop"))

    content += navigation()

    return Page(state, content)


@route
def open_pack(state: State) -> Page:
    price = get_pack_price(state.selected_pack)

    content = [
        Header("OPENING YOUR PACK"),
        "\n"
    ]

    if state.coins < price:
        content.append("You do not have enough coins.")
        content.append(Button("Return to Pack Shop", "pack_shop"))

    else:
        state.coins = state.coins - price
        state.packs_opened += 1
        state.current_pack = []

        for i in range(get_pack_size(state.selected_pack)):
            new_card = generate_card(state.selected_pack)
            state.current_pack.append(new_card)
            state.collection.append(new_card)

        content.append("You opened a " + state.selected_pack + "!")
        content.append("\n")
        content.append(Header("YOUR FIVE NEW CARDS"))

        for card in state.current_pack:
            content.append(card_description(card))
            content.append(rarity_message(card))
            content.append("\n")

        content.append("Coins remaining: " + str(state.coins))
        content.append("Total cards collected: " + str(len(state.collection)))
        content.append("\n")
        content.append(Button("Open Another Pack", "pack_shop"))
        content.append(Button("View My Collection", "collection"))

    content += navigation()

    return Page(state, content)


@route
def collection(state: State, favorites_only: bool = False) -> Page:
    content = [
        Header("MY COLLECTION"),
        "Total cards: " + str(len(state.collection)),
        "Favorite cards: " + str(count_favorites(state.collection)),
        "Rare cards: " + str(count_rare_cards(state.collection)),
        "\n",
        "Check the box to show favorites only:",
        CheckBox("favorites_only", favorites_only),
        Button("Apply Filter", "collection"),
        "\n"
    ]

    found_card = False

    for i in range(len(state.collection)):
        card = state.collection[i]

        if not favorites_only or card.favorite:
            found_card = True

            content.append(Header(card.player_name))
            content.append(card.team + " | " + str(card.year))
            content.append("Position: " + card.position)
            content.append("Rarity: " + card.rarity)

            if card.favorite:
                content.append("Favorite card")

            content.append(
                Button(
                    "View Card Details",
                    "card_details",
                    [Argument("card_index", i)]
                )
            )

            content.append("\n")

    if len(state.collection) == 0:
        content.append(
            "Your collection is empty. Open a pack to get started!"
        )
        content.append(Button("Visit Pack Shop", "pack_shop"))

    elif not found_card:
        content.append("No favorite cards found.")

    content += navigation()

    return Page(state, content)


def build_card_details(state: State, card_index: int) -> Page:
    content = [
        Header("CARD DETAILS"),
        "\n"
    ]

    if card_index < 0 or card_index >= len(state.collection):
        content.append("Card not found.")
        content.append(Button("Return to Collection", "collection"))

    else:
        card = state.collection[card_index]

        content.append(Header(card.player_name))
        content.append("Team: " + card.team)
        content.append("Year: " + str(card.year))
        content.append("Position: " + card.position)
        content.append("Rarity: " + card.rarity)
        content.append(rarity_message(card))
        content.append("\n")

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

        content.append("\n")
        content.append(Button("Return to Collection", "collection"))

    content += navigation()

    return Page(state, content)


@route
def card_details(state: State, card_index: int) -> Page:
    return build_card_details(state, card_index)


@route
def toggle_favorite(state: State, card_index: int) -> Page:
    if 0 <= card_index < len(state.collection):
        card = state.collection[card_index]
        card.favorite = not card.favorite

    return build_card_details(state, card_index)


@route
def search_cards(
    state: State,
    player_search: str = "",
    favorites_only: bool = False
) -> Page:

    player_search = player_search.strip()

    content = [
        Header("SEARCH CARDS"),
        "Search for a player by name.",
        "\n",
        TextBox("player_search", player_search),
        "\n",
        "Search favorites only:",
        CheckBox("favorites_only", favorites_only),
        "\n",
        Button("Search", "search_cards"),
        "\n",
        Header("SEARCH RESULTS")
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

            content.append(Header(card.player_name))
            content.append(card.team + " | " + str(card.year))
            content.append("Rarity: " + card.rarity)

            content.append(
                Button(
                    "View Card Details",
                    "card_details",
                    [Argument("card_index", i)]
                )
            )

            content.append("\n")

    if not found_card:
        if len(state.collection) == 0:
            content.append(
                "You do not have any cards yet. Open a pack first!"
            )
        else:
            content.append("No matching cards were found.")

    content += navigation()

    return Page(state, content)


@route
def collection_stats(state: State) -> Page:
    common_count = 0
    uncommon_count = 0
    rare_count = 0
    legendary_count = 0

    for card in state.collection:
        if card.rarity == "Common":
            common_count += 1
        elif card.rarity == "Uncommon":
            uncommon_count += 1
        elif card.rarity == "Rare":
            rare_count += 1
        elif card.rarity == "Legendary":
            legendary_count += 1

    content = [
        Header("COLLECTION STATISTICS"),
        "Total cards: " + str(len(state.collection)),
        "\n",
        "Common cards: " + str(common_count),
        "Uncommon cards: " + str(uncommon_count),
        "Rare cards: " + str(rare_count),
        "Legendary cards: " + str(legendary_count),
        "\n",
        "Favorite cards: " + str(count_favorites(state.collection)),
        Button("Return to Collection", "collection")
    ]

    content += navigation()

    return Page(state, content)


start_server(
    State(
        coins=500,
        packs_opened=0,
        collection=[],
        current_pack=[],
        selected_pack="Rookie Pack"
    )
)
