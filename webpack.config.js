const webpack = require('webpack');
const config = {
    entry:  [__dirname + '/assets/scripts/index.js'],
    output: {
        path: __dirname,
        filename: 'static/backend_theme/js/bundle.js',
    },
    resolve: {
        extensions: ['.js']
    },
    module: {
        loaders: [
            {
                test: /\.js?/,
                exclude: /node_modules/,
                use: 'babel-loader'
            }
        ]
    }
};
module.exports = config;