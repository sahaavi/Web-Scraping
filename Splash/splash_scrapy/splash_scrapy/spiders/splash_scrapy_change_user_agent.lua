function main(splash, args)
    -- Change User-Agent (Option 1)
    --splash: set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82')

    -- Change User-Agent (Option 2)
    --[[
        headers = {
        [
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'
    }
    splash: set_custom_headers(headers)
            - -]]

    -- Change User-Agent (Option 3)
    splash: on_request(function(request)
    request: set_header('User-Agent',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82')
    end)

    -- If a website doesn't render correctly, disabling Private mode might help
    splash.private_mode_enabled = false
    -- Go to the URL set on the splash browser and then wait 3 seconds to let the page render
    assert(splash:go(args.url))
    assert(splash:wait(3))
    -- Select all the elements that have the css selector "label.btn.btn-sm.btn-primary"
    all_matches = assert(splash:select_all("label.btn.btn-sm.btn-primary"))
    -- Two elements were selected. We want to click on the second button, then wait 3 seconds to let the page render
    all_matches[2]: mouse_click()
    assert (splash:wait(3))
    -- Increase the viewport to make all the content visible
    splash: set_viewport_full()
    return {splash: png(), splash: html()}
end