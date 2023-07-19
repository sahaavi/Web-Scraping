-- website: https://www.amazon.com/

function main(splash, args)
    -- Setting the url
    url = args.url
    -- Go to the url and then wait 2 seconds to let the page render correctly
    assert (splash:go(url))
    assert (splash:wait(1))

    -- Select the text box with the css selector "#twotabsearchtextbox"
    input_box = assert(splash:select("#twotabsearchtextbox"))
    -- We can’t assume that the element we want will be focused so use ":focus()"
    input_box:focus()
    -- Send text and wait 1 second to let the page render correctly (you can add more time if needed)
    input_box:send_text("books")
    assert(splash:wait(1))

    -- Select the search button with the css selector "#nav-search-submit-button", click on it and wait 5 seconds
    button = assert(splash:select("#nav-search-submit-button"))
    button:mouse_click()
    assert(splash:wait(5))
    return {
        html = splash:html(),
        png = splash:png(),
    }
end