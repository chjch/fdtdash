html_layout = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link
            rel="stylesheet"
            href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
        />
    </head>
    <body>
        <div class='splash'>
            <div class='logo'>
                <div class="logo-text">
                    <h1 class='animate__animated animate__fadeIn animate__delay-1s'>Jax</h1>
                    <h1 class='animate__animated animate__fadeIn animate__delay-3s'>Twin.</h1>
                </div>
                <img class='logo-image' src='/jtdash/assets/images/splash-logo-image.png'/>
            </div>
        </div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''