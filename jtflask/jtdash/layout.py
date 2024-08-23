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
        {%app_entry%}
        <div class='splash'>
            <div class='logo'>
                <h1 class='animate__animated animate__fadeInDown'>Jax</h1>
                <h1 class='animate__animated animate__fadeInUp animate__delay-1s'>Twin</h1>
            </div>
            <img class='logo-image animate__animated animate__fadeIn' src='/jtdash/assets/images/splash-logo-image.png' hidden="true"/>
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''