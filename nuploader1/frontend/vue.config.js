if (process.env.NODE_ENV === 'production') {
    module.exports = {
        outputDir: '../static',
        assetsDir: '../static/nuploader1',
        indexPath: '../templates/nuploader1/index.html',
        publicPath: '/uploader/',
    };

}