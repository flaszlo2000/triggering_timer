- [] timer:  
    - [x] timers can be added
    - [x] reports back current timers
    - [x] ws realtime reporting
    - [x] can cancel timer

    - [] UI
        - [x] add scrollbar
        - [x] use friendly names
        - [] if the user clicks out on the UI when the dropdown is open, close the dropdown
        - [] advertise custrom cards to show up in HA automatically
        - [] make dropdown interchangable to entities
        - [] make dropdown area sensitive
        - [] make time editabe
            - [x] added button
            - [] added popup
            - [] timer can be updated
        - [] send notification ?
        - [] ordering
            - [] make order changable on ui
            - [] make backend remember the order
        - [] change cancel button to cancel icon-button
        - [] clicking on automation name (or line itself) navigates to the automation
    - [] hacs
        - [] added translation but use it too
        - [x] added via custom repository
        - [] integration:
            - [] remove the need to extend configuration.yaml
    - [] make back counter nicer:
        - [x] real time count back
        - [] instead of count back, progressbar ?
        - [] start -only on the UI- timer with an additional +1 sec to avoid any lag at 00:00:00
        - [] dont show any piece of time that is zero
    
    - [] BACKEND:
        - [] Fader
            - [] add Timer like Fader
            - [] use multiple timing methods
        - [] binary sensor with automation_id that represents that if we have a timer to the corresponding automation_id
        - [] add entity that enables other stuff (other the the ui) to interact with the backend entity (works but schema must be update to enable HA to hint the needed fields, bug maybe? )

    - [] git
        - [] add images
        - [] add proper readme
            - [] ui
            - [] integration

        - [] make workflow not fail with ui

- bugs:
    - [x] fix error that makes temp sensor ui infinite load after visiting timer ui
    - [x] fix ping error
    - [x] fix subscribeMessage null error

    - UI:
        - [x] fix issue with too big names overflowing
    
    - [] fix timezone
    - [] fix services.yaml
