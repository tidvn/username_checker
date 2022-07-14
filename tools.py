#!/usr/bin/env python3
import asyncio
import logging
import maigret
# import WhatsMyName.web_accounts_list_checker

# top popular sites from the Maigret database
TOP_SITES_COUNT = 300 #3025
# Maigret HTTP requests timeout
TIMEOUT = 10
# max parallel requests
MAX_CONNECTIONS = 50


if __name__ == '__main__':
    # setup logging and asyncio
    logger = logging.getLogger('maigret')
    logger.setLevel(logging.WARNING)
    loop = asyncio.get_event_loop()
    db = maigret.MaigretDatabase().load_from_file('./maigret/resources/data.json')

    username = 'tidvn'
    sites_count = TOP_SITES_COUNT
    sites = db.ranked_sites_dict(top=sites_count)
    show_progressbar = True
    extract_info = True
    use_notifier = None
    notifier = None
    if use_notifier:
        notifier = maigret.Notifier(print_found_only=True, skip_check_errors=True)

    # search!
    search_func = maigret.search(
        username=username,
        site_dict=sites,
        timeout=TIMEOUT,
        logger=logger,
        max_connections=MAX_CONNECTIONS,
        query_notify=notifier,
        no_progressbar=(not show_progressbar),
        is_parsing_enabled=extract_info,
    )

    results = loop.run_until_complete(search_func)


    for sitename, data in results.items():
        is_found = data['status'].is_found()
        print(f'{sitename} - {"Found!" if is_found else "Not found"}')
