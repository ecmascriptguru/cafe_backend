var webpack = require("webpack"),
    path = require("path"),
    fileSystem = require("fs"),
    CleanWebpackPlugin = require("clean-webpack-plugin"),
    CopyWebpackPlugin = require("copy-webpack-plugin"),
    // HtmlWebpackPlugin = require("html-webpack-plugin"),
    WriteFilePlugin = require("write-file-webpack-plugin");

// load the secrets
var alias = {};

var secretsPath = path.join(__dirname, ("secrets." + ".js"));

var imageFileExtensions = ["jpg", "jpeg", "png", "gif", "svg"]
var fontFileExtensions = ["eot", "otf", "ttf", "woff", "woff2", "svg"];

if (fileSystem.existsSync(secretsPath)) {
  alias["secrets"] = secretsPath;
}

var options = {
//   mode: "development",
  entry: {
    index: path.join(__dirname, "assets", "scripts", "index.js"),
    // popup: path.join(__dirname, "src", "js", "popup.js"),
  },
  output: {
    path: path.join(__dirname, "static"),
    filename: "js/[name].js"
  },
  module: {
    rules: [
      {
        test: /\.(ttf|eot|svg|woff2?)(\?v=[a-z0-9=\.]+)?$/i,
        // exclude: /node_modules/,
        loader: 'url-loader?limit=1024&name=fonts/[name].[ext]'
      },
      {
        test: /\.css$/,
        loader: "style-loader!css-loader",
        exclude: /node_modules/
      },
      {
        test: new RegExp('\.(' + imageFileExtensions.join('|') + ')$'),
        loader: "file-loader?name=img/[name].[ext]",
        // exclude: /node_modules/
      },
    //   { test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/ }
    ]
  },
  resolve: {
    alias: alias
  },
  plugins: [
    // clean the build folder
    new CleanWebpackPlugin(["static"]),
    // expose and write the allowed env vars on the compiled bundle
    // new webpack.EnvironmentPlugin(["NODE_ENV"]),
    new CopyWebpackPlugin([]),
    new WriteFilePlugin()
  ]
};

module.exports = options;
