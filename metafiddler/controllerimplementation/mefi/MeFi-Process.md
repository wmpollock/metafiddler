# Reverse-engineering favorite

Backtraced from google in Oct 2019:

POST: https://music.metafilter.com/contribute/track-add.mefi

Doesn't look like much has changed from here:
https://metatalk.metafilter.com/15745/What-cookies-do-I-need-to-set-in-order-to-have-a-console-app-grab-my-usersnear-page

They suggest mechanising the login which is cool and all yes, but not quite as expedient as ripping into cookies.

The <https://metatalk.metafilter.com/15745/What-cookies-do-I-need-to-set-in-order-to-have-a-console-app-grab-my-usersnear-page#509461 observed values necessary> were:
   USER_TOKEN, USER_ID and USER_NAME

## form fields:
link_id: numeric post ID  
playlist_id: playlist ID #  
playlist_name: null for existing  
playlist_description: null for existing  
post: Add to Playlist