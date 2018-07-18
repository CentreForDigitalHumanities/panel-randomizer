module.exports = {
    entry: './scripts/youtube-helper.ts',
    output: {
        filename: './panel_randomizer_app/static/scripts/youtube-helper.js',
        libraryTarget: 'umd'
    },
    devtool: "source-map",
    resolve: {
        extensions: ['.ts', '.tsx', '.js']
    },
    module: {
        loaders: [
            {
                test: /\.tsx?$/,
                loader: 'ts-loader'
            }
        ]
    }
}
