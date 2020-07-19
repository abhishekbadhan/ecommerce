console.log('this is running')
script = document.createElement('script')
script.type = 'text/javascript'
script.src = 'https://cdn.tiny.cloud/1/b4o30dm98lz9234l6an729zohsyy26h4rbmmxtfwncig4pfa/tinymce/5/tinymce.min.js'
document.head.appendChild(script)


console.log('this is console log7')

script.onload = function() {
    tinymce.init({
        selector: '#id_product_desc',
        width: 800,
        height: 400,
        plugins: [
            'advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker',
            'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
            'table emoticons template paste help'
        ],
        toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | ' +
            'bullist numlist outdent indent | link image | print preview media fullpage | ' +
            'forecolor backcolor emoticons | help',
        menu: {
            favs: {
                title: 'My Favorites',
                items: 'code visualaid | searchreplace | spellchecker | emoticons'
            }
        },
        menubar: 'favs file edit view insert format tools table help',
        content_css: 'css/content.css'
    });
}