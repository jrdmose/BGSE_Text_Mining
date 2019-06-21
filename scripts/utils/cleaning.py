import re
from bs4 import BeautifulSoup
import emoji

# Function for identifying cyrillic text using regex
def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

# Checking for arabic characters
def has_arabic(text):
    return bool(re.search('[ا-ي]', text))

def remove_emoji(text):

    # Pattern
    emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                u"\U0001f926-\U0001f937"
                u'\U00010000-\U0010ffff'
                u"\u200d"
                u"\u2640-\u2642"
                u"\u2600-\u2B55"
                u"\u23cf"
                u"\u23e9"
                u"\u231a"
                u"\u3030"
                u"\ufe0f"
    "]+", flags=re.UNICODE)

    # Removal
    return re.sub(emoji_pattern,'',text)

# Functoin for cleaning the single tweets
def clean_tweet(s):

    # Use BeautifulSoup to remove extrap whitespace and convert to lowerspace
    s = BeautifulSoup(s,'html5lib').get_text()

    # Whitespace
    s = ' '.join(s.split())

    # Lowercase
    s = s.strip().lower()

    # Substitute &
    s = re.sub("&amp;", "and",s) # &

    # Pattern for cleaning the tweets
    clean_pattern = [r'(@\w+=?:?)', #Mentions
                         r'(rt)', # Retweets
                         r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', # urls
                         r'(https)', # left over
                         r'(\n)', # Break lines
                         r'[(]|[)]',# Parenthesis
                         r'(&w\+)']



    clean_pattern = '|'.join(clean_pattern)

    # Use pattern to return cleaned string
    s = re.sub(clean_pattern,'',s)

    # Clean emojis
    s =  remove_emoji(s)

    # Clean the hashtags, but just remove # not the tag itself
    s = s.replace("#", "")

    return s
