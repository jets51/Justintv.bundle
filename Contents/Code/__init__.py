# PMS plugin framework
# Justin.tv Plugin 
# v0.1 by Trevor Cortez <trevor.cortez@gmail.com>
# Updated v0.2 onwards by John Roberts : 41john
# http://wiki.plexapp.com/index.php/Justin.tv


####################################################################################################

VIDEO_PREFIX = "/video/justintv"
JTV_LIST_STREAMS = "http://api.justin.tv/api/stream/list.json"
JTV_FAVOURITE = "http://api.justin.tv/api/user/favorites/%s.json"
JTV_SWF_PLAYER = "http://www.justin.tv/widgets/live_api_player.swf"
CACHE_INTERVAL  = 3600
CACHE_INTERVAL_FAV  = 600
CONSUMER_KEY = "RVlO2N4ySXlhy0z0DXXKQ"
NAME = L('Title')

# make sure to replace artwork with what you want
# these filenames reference the example files in
# the Contents/Resources/ folder in the bundle
ART           = 'art-default4.png'
ICON          = 'icon-default1.png'

####################################################################################################

def Start():

    ## make this plugin show up in the 'Video' section
    ## in Plex. The L() function pulls the string out of the strings
    ## file in the Contents/Strings/ folder in the bundle
    ## see also:
    ##  http://dev.plexapp.com/docs/mod_Plugin.html
    ##  http://dev.plexapp.com/docs/Bundle.html#the-strings-directory
    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, L('VideoTitle'), ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    ## set some defaults so that you don't have to
    ## pass these parameters to these object types
    ## every single time
    ## see also:
    ##  http://dev.plexapp.com/docs/Objects.html
    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)

  


#### the rest of these are user created functions and
#### are not reserved by the plugin framework.
#### see: http://dev.plexapp.com/docs/Functions.html for
#### a list of reserved functions above



#
# Example main menu referenced in the Start() method
# for the 'Video' prefix handler
#

def VideoMainMenu():

    # Container acting sort of like a folder on
    # a file system containing other things like
    # "sub-folders", videos, music, etc
    # see:
    #  http://dev.plexapp.com/docs/Objects.html#MediaContainer
    dir = MediaContainer(viewGroup="InfoList")

    dir.Append(
        Function(
            DirectoryItem(
                CategoriesMenu,
                "Categories",
                "",
                summary="Browse live streams by category",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
  
    # Part of the "search" example 
    # see also:
    #   http://dev.plexapp.com/docs/Objects.html#InputDirectoryItem
    dir.Append(
        Function(
            InputDirectoryItem(
                SearchResults,
                "Search...",
                "",
                summary="Search for a stream",
                thumb=R("search.png"),
                art=R(ART)
            )
        )
    )

    # The Favourite menu item
    dir.Append(
        Function(
            DirectoryItem(
                Favourites,
                "Favourites",
                "",
                summary="Favourite Streams",
                thumb=R("Favorite.png"),
                art=R(ART)
            )
        )
    )
    
    dir.Append(PrefsItem(L("Preferences..."), thumb=R("icon-prefs.png")))

    # ... and then return the container
    
    return dir

def CategoriesMenu(sender):
    dir = MediaContainer(viewGroup="List",title2="Categories")
    categories = {'featured': 'Featured', '': 'All', 'social': 'Social', 'entertainment':'Entertainment', 'gaming':'Gaming', 'sports':'Sports', 'news':'News & Events', 'animals':'Animals', 'science_tech':'Science & Technology', 'educational':'Educational', 'other':'Other'}
    orderedCategories = ['','featured','social','entertainment','gaming','sports','news','animals','science_tech','educational','other']
    for category in orderedCategories:
        dir.Append(
            Function(
                DirectoryItem(
                    ChannelMenu,
                    categories[category],
                    subtitle="",
                    summary="",
                    thumb=R(ICON),
                    art=R(ART),
                ),url="%s?category=%s" % (JTV_LIST_STREAMS, category)
            )
        )
    return dir    

def ChannelMenu(sender,url=None):
    dir = MediaContainer(viewGroup="InfoList",title2=sender.itemTitle)
    json = JSON.ObjectFromURL(url,cacheTime=CACHE_INTERVAL)
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

# Part of the "search" example 
# query will contain the string that the user entered
# see also:
#   http://dev.plexapp.com/docs/Objects.html#InputDirectoryItem
def SearchResults(sender,query=None):
    dir = MediaContainer(viewGroup="InfoList")
    json = JSON.ObjectFromURL(JTV_LIST_STREAMS,cacheTime=CACHE_INTERVAL)
    
    for stream in json:
      try:
        sTitle = stream["title"]
        sSummary = stream["channel"]["status"]
        sSubtitle = " %s Viewers" % stream["stream_count"]
        sStreamURL = "%s" % stream["channel"]["channel_url"]
        if (sTitle.upper().find(query.upper()) != -1):
          dir.Append(WebVideoItem(sStreamURL, title=sTitle, summary=sSummary, subtitle=sSubtitle, thumb=stream["channel"]["image_url_huge"], duration=0))
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
    dir = MediaContainer(viewGroup="InfoList")
    json = JSON.ObjectFromURL(JTV_FAVOURITE%Prefs['username'],cacheTime=CACHE_INTERVAL_FAV)
    for stream in json:
        try:
            sTitle = stream["title"]
            sSummary = stream["status"]
            sStreamURL = "%s" % stream["channel_url"]
            dir.Append(WebVideoItem(sStreamURL, title=sTitle, summary=sSummary, thumb=stream["image_url_huge"], duration=0))
        except:
            pass
    return dir
    
def sortedDictValues1(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items]

