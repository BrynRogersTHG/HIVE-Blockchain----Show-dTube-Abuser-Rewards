
# Show Dtube Abuser Rewards
# @slobberchops - February 2023

from datetime import datetime, timedelta
from beem import Hive
from beem.account import Account
from beem.comment import Comment
from beem.exceptions import ContentDoesNotExistsException
from beem.instance import set_shared_blockchain_instance
import os

badtag = "dtube"
version = "1.1"
stop = datetime.utcnow() - timedelta(days=6.9)
os.system("")

activenode = ["https://api.deathwing.me"]
hive = Hive(node=activenode)
set_shared_blockchain_instance(hive)

# ---------------------------------------------------------

# StdOut console colour definitions
class bcolors:
     HEADER = '\033[95m'
     BLUE = '\033[94m'
     CYAN = '\033[96m'
     GREEN = '\033[92m'
     YELLOW = '\033[93m'
     VIOLET = '\033[35m'
     RED = '\033[91m'
     END = '\033[0m'
     BOLD = '\033[1m'
     UNDERLINE = '\033[4m'
# ---------------------------------------------------------
# --------------------------------------------------------------------------------------------
# Function getpost (account)
# Returns ALL pending posts that could get voted as a BEEMComment object

def getactivedtubeposts (account):

    dtubeposts = []
    c_list = {}
    post_counter = 0
    mypost = ""

    try:
        for post in map(Comment, account.history_reverse(stop=stop, only_ops=['comment'], use_block_num=False)):

            if post.permlink in c_list:
                continue
            try:
                post.refresh()
            except ContentDoesNotExistsException:
                continue
            c_list[post.permlink] = 1

            # Skip anything that is NOT a post and is NOT pending rewards
            if not post.is_comment() and post.is_pending():
                if detecttag(post, badtag):
                    dtubeposts.append(post)
    except:
        print(bcolors.RED + "HIVE Blockchain timeout error, recalibrating..." + bcolors.END)

    return dtubeposts
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# Function: detecttag  - Tag Detector (strcomment, strnovotetag)
# Returns a Boolean Value (True) if the post contains
# the tag strnovotetag
# --------------------------------------------------------------------------------------------
def detecttag(strpost, strnovotetag):

    c = Comment(strpost)
    taglist = strpost["tags"]
    for item in taglist:
        if item == strnovotetag:
            return True

    return False
# --------------------------------------------------------------------------------------------

# Main Script

os.system('cls')

abusers = ["abuser1", "abuser2", "abuser3"]

print()
print(bcolors.CYAN + f'Show dTube Abuser Rewards {version} - @slobberchops (February 2023)' + bcolors.END)
print (bcolors.VIOLET + f' Active Node is {activenode}' + bcolors.END)
print()

for abuser in abusers:
    outstandingrewards = 0
    outstandingposts = 0
    account = Account(abuser)
    dtubepostsposts = getactivedtubeposts(account)

    for post in dtubepostsposts:
        outstandingposts += 1
        rewards = str(post.get_author_rewards()["payout_SP"])
        floatrewards = float(rewards[:5])
        outstandingrewards += floatrewards

    if outstandingposts > 0:
        if outstandingrewards > 0.00:
            print(bcolors.RED + f'*** The account {abuser} has pending {outstandingposts} posts, and rewards of {outstandingrewards} HIVE so needs blasting! ***' + bcolors.END)
        else:
            print(bcolors.GREEN + f'...The account {abuser} has pending {outstandingposts} posts and zero rewards pending...' + bcolors.END)

os.system('pause')


