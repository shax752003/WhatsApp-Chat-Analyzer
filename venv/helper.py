from urlextract import URLExtract
extract = URLExtract()
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    #fetch no of words
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
            words.extend(message.split())
    #fetch no of images
    num_images = df[df['message']=='image omitted\n'].shape[0]

    #fetch no of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_images,len(links)

def most_active_users(df):
    x = df['user'].value_counts().head()
    return x 




    
 


















