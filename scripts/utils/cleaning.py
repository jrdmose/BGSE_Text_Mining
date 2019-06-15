import re
from bs4 import BeautifulSoup
import emoji

# Function for identifying cyrillic text using regex
def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

# Checking for arabic characters
def has_arabic(text):
    return bool(re.search('[ا-ي]', text))

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
                         r'(#\w+)', # tags
                         r'(&w\+)']

    clean_pattern = '|'.join(clean_pattern)

    # Use pattern to return cleaned string
    s = re.sub(clean_pattern,'',s)

    # Convert emojis to text
    s = emoji.demojize(s)



    return s
