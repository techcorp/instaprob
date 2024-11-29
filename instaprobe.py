import instaloader
import os
import time
from termcolor import colored

# Function to display the banner with the tool name and YouTube channel
def display_banner():
    os.system("cls" if os.name == "nt" else "clear")  # Clear the screen for a cleaner output

    # Stylish ASCII banner for the tool name
    banner = """ 
 /$$$$$$                       /$$               /$$$$$$$                      /$$      
|_  $$_/                      | $$              | $$__  $$                    | $$      
  | $$   /$$$$$$$   /$$$$$$$ /$$$$$$    /$$$$$$ | $$  \ $$  /$$$$$$   /$$$$$$ | $$$$$$$ 
  | $$  | $$__  $$ /$$_____/|_  $$_/   |____  $$| $$$$$$$/ /$$__  $$ /$$__  $$| $$__  $$
  | $$  | $$  \ $$|  $$$$$$   | $$      /$$$$$$$| $$____/ | $$  \__/| $$  \ $$| $$  \ $$
  | $$  | $$  | $$ \____  $$  | $$ /$$ /$$__  $$| $$      | $$      | $$  | $$| $$  | $$
 /$$$$$$| $$  | $$ /$$$$$$$/  |  $$$$/|  $$$$$$$| $$      | $$      |  $$$$$$/| $$$$$$$/
|______/|__/  |__/|_______/    \___/   \_______/|__/      |__/       \______/ |_______/ 
                                                                                        
                                                                                        
                                                                                                     
    """

    print(colored(banner, "yellow", attrs=["bold"]))
    print(colored("Created by Technical Corp", "green"))
    print(colored("YouTube: youtube.com/@technicalcorp", "blue"))
    print(colored("-" * 50, "green"))

# Function to save info to a file and display on the screen
def save_and_display_info(account, data, filename):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_path = f"{account}_{filename}_{timestamp}.txt"

    # Save data to file
    with open(file_path, "w") as file:
        for item in data:
            file.write(f"{item}\n")

    print(f"\n[INFO] Data saved to {file_path}\n")

    # Display the data on the screen
    print("[INFO] Data gathered:")
    for item in data:
        print(item)

# Function to download media (photos, stories)
def download_media(L, profile, media_type="photos"):
    if media_type == "photos":
        for post in profile.get_posts():
            if post.is_video:
                print(f"Skipping video: {post.url}")
                continue
            L.download_post(post, target=profile.username)
    elif media_type == "stories":
        for story in L.get_stories():
            for item in story.get_items():
                L.download_storyitem(item, target=profile.username)

# Function to fetch Instagram info
def fetch_instagram_info(target_account, login_required=False):
    L = instaloader.Instaloader()

    try:
        # If login is required, load session or login
        if login_required:
            if os.path.exists(f"{target_account}_session"):
                L.load_session_from_file(target_account)
            else:
                username = input("Enter your Instagram username: ")
                password = input("Enter your Instagram password: ")
                L.login(username, password)  # Login to Instagram
                L.save_session_to_file()

        # Fetch profile data
        profile = instaloader.Profile.from_username(L.context, target_account)

        # Display basic info about the profile
        print(f"\nProfile Information for @{target_account}:")
        print(f"Full Name: {profile.full_name}")
        print(f"Bio: {profile.biography}")
        print(f"Total Posts: {profile.mediacount}")
        print(f"Followers: {profile.followers}")
        print(f"Following: {profile.followees}\n")

        if login_required:
            # Ask the user for what data to fetch if logged in
            print("Choose the data you want to gather:")
            print("1. Captions")
            print("2. Comments")
            print("3. Followers")
            print("4. Followings")
            print("5. Hashtags")
            print("6. Likes")
            print("7. Media Type")
            print("8. Photo Descriptions")
            print("9. Photos (Download)")
            print("10. Profile Picture (Download)")
            print("11. Stories (Download)")
            print("12. Tagged Users")
            print("13. Users Who Commented")
            print("14. Users Who Tagged")

            choice = input("Enter choice (1-14): ")

            # Collecting data based on user choice
            if choice == "1":  # Captions
                captions = [post.caption for post in profile.get_posts()]
                save_and_display_info(target_account, captions, "captions")
            elif choice == "2":  # Comments
                comments = [len(post.get_comments()) for post in profile.get_posts()]
                save_and_display_info(target_account, comments, "comments")
            elif choice == "3":  # Followers
                followers = [follower.username for follower in profile.get_followers()]
                save_and_display_info(target_account, followers, "followers")
            elif choice == "4":  # Followings
                following = [following.username for following in profile.get_followees()]
                save_and_display_info(target_account, following, "followings")
            elif choice == "5":  # Hashtags
                hashtags = set()
                for post in profile.get_posts():
                    hashtags.update(post.caption_hashtags)
                save_and_display_info(target_account, list(hashtags), "hashtags")
            elif choice == "6":  # Likes
                likes = [post.likes for post in profile.get_posts()]
                save_and_display_info(target_account, likes, "likes")
            elif choice == "7":  # Media Type
                media_types = ["Video" if post.is_video else "Photo" for post in profile.get_posts()]
                save_and_display_info(target_account, media_types, "mediatypes")
            elif choice == "8":  # Photo Descriptions
                descriptions = [post.caption for post in profile.get_posts()]
                save_and_display_info(target_account, descriptions, "photodes")
            elif choice == "9":  # Photos (Download)
                download_media(L, profile, media_type="photos")
            elif choice == "10":  # Profile Picture (Download)
                L.download_profilepic(profile)
            elif choice == "11":  # Stories (Download)
                download_media(L, profile, media_type="stories")
            elif choice == "12":  # Tagged Users
                tagged_users = set()
                for post in profile.get_posts():
                    tagged_users.update(post.tagged_users)
                save_and_display_info(target_account, list(tagged_users), "tagged")
            elif choice == "13":  # Users Who Commented
                commented_users = set()
                for post in profile.get_posts():
                    commented_users.update([commenter.username for commenter in post.get_comments()])
                save_and_display_info(target_account, list(commented_users), "wcommented")
            elif choice == "14":  # Users Who Tagged
                tagged_users = set()
                for post in profile.get_posts():
                    tagged_users.update([tagged.username for tagged in post.get_tags()])
                save_and_display_info(target_account, list(tagged_users), "wtagged")
            else:
                print("[ERROR] Invalid choice. Please select a valid option.")
        else:
            # If login is not required, display only basic info
            print("[INFO] Login not required. Displaying basic public information.")
            print(f"Full Name: {profile.full_name}")
            print(f"Bio: {profile.biography}")
            print(f"Total Posts: {profile.mediacount}")
            print(f"Followers: {profile.followers}")
            print(f"Following: {profile.followees}")

            # Ask user if they want to gather more advanced info
            advanced_choice = input("\nDo you want to gather more advanced info (login required)? (yes/no): ").lower()
            if advanced_choice == "yes":
                login_required = True
                fetch_instagram_info(target_account, login_required)
            else:
                print("[INFO] Exiting with basic information.")

            return  # Exit function after basic info

        # Ask if the user wants to gather more data
        more_data = input("\nDo you want to gather more data? (yes/no): ").lower()
        if more_data == "yes":
            fetch_instagram_info(target_account, login_required)
        else:
            print(colored("[INFO] Goodbye!", "red"))
            exit()

    except Exception as e:
        print(f"\n[ERROR] {e}")

def show_menu():
    display_banner()
    print(colored("Choose an option:", "yellow"))
    print("1. Gather Instagram Information (Login Required for advanced features)")
    print("2. Exit")
    choice = input("Enter choice (1/2): ")

    if choice == "1":
        target_account = input("Enter the Instagram account to gather information from: ")
        login_choice = input("Do you want to login for followers and followings? (yes/no): ").lower()
        login_required = login_choice == "yes"
        fetch_instagram_info(target_account, login_required)
    else:
        print(colored("[INFO] Goodbye!", "red"))
        exit()

if __name__ == "__main__":
    while True:
        show_menu()
