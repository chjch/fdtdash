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
                <h1 class='animate__animated animate__fadeInUp'>Twin</h1>
            </div>
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''