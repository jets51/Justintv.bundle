# Justin.tv Plugin 
# v0.1 by Trevor Cortez <trevor.cortez@gmail.com>
# Updated v0.2 onwards by John Roberts : 41john
# http://wiki.plexapp.com/index.php/Justin.tv

####################################################################################################

JTV_LIST_STREAMS = "http://api.justin.tv/api/stream/list.json"
JTV_FAVOURITE = "http://api.justin.tv/api/user/favorites/%s.json"
JTV_SWF_PLAYER = "http://www.justin.tv/widgets/live_api_player.swf"
CACHE_INTERVAL = 3600
CACHE_INTERVAL_FAV = 600
NAME = "Justin.tv"
ART = "art-default.jpg"
ICON = "icon-default.png"

####################################################################################################
def Start():
    Plugin.AddPrefixHandler("/video/justintv", VideoMainMenu, NAME, ICON, ART)
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "InfoList"
    DirectoryItem.thumb = R(ICON)

def VideoMainMenu():
    dir = MediaContainer(noCache=True)
    dir.Append(Function(DirectoryItem(CategoriesMenu, title="Categories", summary="Browse live streams by category")))
    dir.Append(Function(InputDirectoryItem(SearchResults, title="Search...", prompt="Search for a stream", thumb=R("icon-search.png"))))
    if Prefs['username']:
        dir.Append(Function(DirectoryItem(Favourites, title="Favourites", summary="Favourite Streams", thumb=R("icon-favorite.png"))))
    dir.Append(PrefsItem(title="Preferences...", thumb=R("icon-prefs.png")))
    return dir

def CategoriesMenu(sender):
    dir = MediaContainer(viewGroup="List", title2="Categories")
    categories = {'featured': 'Featured', 'social': 'Social', 'entertainment':'Entertainment', 'gaming':'Gaming', 'sports':'Sports', 'news':'News & Events', 'animals':'Animals', 'science_tech':'Science & Technology', 'educational':'Educational', 'other':'Other'}
    orderedCategories = ['featured','social','entertainment','gaming','sports','news','animals','science_tech','educational','other']
    for category in orderedCategories:
        dir.Append(Function(DirectoryItem(ChannelMenu, title=categories[category]) ,url="%s?category=%s" % (JTV_LIST_STREAMS, category)))
    return dir

def ChannelMenu(sender, url=None):
    dir = MediaContainer(title2=sender.itemTitle)
    json = JSON.ObjectFromURL(url, cacheTime=CACHE_INTERVAL)
    for stream in json:
        try:
            sTitle = stream["title"]
            sSummary = stream["channel"]["status"]
            sSubtitle = " %s Viewers" % stream["stream_count"]
            sStreamURL = "%s" % stream["channel"]["channel_url"]
            dir.Append(WebVideoItem(sStreamURL, title=sTitle, summary=sSummary, subtitle=sSubtitle, thumb=stream["channel"]["image_url_huge"], duration=0))
        except:
            pass
    return dir

def SearchResults(sender, query=None):
    dir = MediaContainer()
    json = JSON.ObjectFromURL(JTV_LIST_STREAMS, cacheTime=CACHE_INTERVAL)

    for stream in json:
        try:
            sTitle = stream["title"]
            sSummary = stream["channel"]["status"]
            sSubtitle = " %s Viewers" % stream["stream_count"]
            sStreamURL = "%s" % stream["channel"]["channel_url"]
            if (sTitle.upper().find(query.upper()) != -1):
                dir.Append(WebVideoItem(sStreamURL, title=sTitle, summary=sSummary, subtitle=sSubtitle, thumb=stream["channel"]["image_url_huge"]))
        except:
            pass
    if len(dir) > 0:
        return dir
    else:
        return MessageContainer(
            "Not found",
            "No streams were found that match your query."
        )

# The Favourites menu 
def Favourites(sender):
    dir = MediaContainer()
    json = JSON.ObjectFromURL(JTV_FAVOURITE%Prefs['username'],cacheTime=CACHE_INTERVAL_FAV)
    for stream in json:
        try:
            sTitle = stream["title"]
            sSummary = stream["status"]
            sStreamURL = "%s" % stream["channel_url"]
            dir.Append(WebVideoItem(sStreamURL, title=sTitle, summary=sSummary, thumb=stream["image_url_huge"]))
        except:
            pass
    return dir
