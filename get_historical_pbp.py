import hockey_scraper

seasons = [2011]
for season in seasons:
    try:
        hockey_scraper.scrape_seasons([season], True)
    except:
        print('Failed to scrape season {}'.format(season))
        continue
