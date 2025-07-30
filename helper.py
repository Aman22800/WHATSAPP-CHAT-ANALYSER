from urlextract import URLExtract
extract = URLExtract()

def fetch_stats(user, df):
    user = user.strip().lower()
    media_indicators = ['<media omitted>', 'image omitted', 'video omitted']

    if user == "overall":
        num_messages = df.shape[0]

        # Word count
        words = []
        for message in df['message']:
            words.extend(message.split())
        num_words = len(words)

        # Media message counts
        num_media_messages = df[df['message'].str.lower().isin(media_indicators)].shape[0]
        num_image_messages = df[df['message'].str.lower() == 'image omitted'].shape[0]
        num_video_messages = df[df['message'].str.lower() == 'video omitted'].shape[0]

        # Non-media messages
        num_non_media_messages = df[~df['message'].str.lower().isin(media_indicators)].shape[0]

        # Links
        links = []
        for message in df['message']:
            links.extend(extract.find_urls(message))

        return num_messages, num_words, num_media_messages, num_image_messages, num_video_messages, num_non_media_messages, len(links)

    else:
        user_df = df[df['user'].str.lower() == user]
        num_messages = user_df.shape[0]

        # Word count
        words = []
        for message in user_df['message']:
            words.extend(message.split())
        num_words = len(words)

        # Media message counts
        num_media_messages = user_df[user_df['message'].str.lower().isin(media_indicators)].shape[0]
        num_image_messages = user_df[user_df['message'].str.lower() == 'image omitted'].shape[0]
        num_video_messages = user_df[user_df['message'].str.lower() == 'video omitted'].shape[0]

        # Non-media messages
        num_non_media_messages = user_df[~user_df['message'].str.lower().isin(media_indicators)].shape[0]

        # Links
        links = []
        for message in user_df['message']:
            links.extend(extract.find_urls(message))

        return num_messages, num_words, num_media_messages, num_image_messages, num_video_messages, num_non_media_messages, len(links)
