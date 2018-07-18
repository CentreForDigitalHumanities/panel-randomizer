var typescriptConfig = require('./tsconfig.json');
typescriptConfig.compilerOptions.allowJs = true;
typescriptConfig.compilerOptions.declaration = false;
typescriptConfig.compilerOptions.strictNullChecks = false;
module.exports = function (config) {
    let configuration = {
        basePath: '',
        frameworks: ['jasmine', 'karma-typescript'],
        files: ['scripts/**/*.+(js|ts)'],
        preprocessors: {
            'scripts/**/*.+(js|ts)': ['karma-typescript']
        },
        reporters: ['progress', 'karma-typescript'],
        autoWatch: false,
        singleRun: true,
        plugins: [
            'karma-chrome-launcher',
            'karma-jasmine',
            'karma-typescript'
        ],
        karmaTypescriptConfig: {
            compilerOptions: typescriptConfig.compilerOptions,
            bundlerOptions: {
                entrypoints: /\.spec\.ts$/
            }
        },
        browsers: ['ChromeHeadless'],
        customLaunchers: {
            Chrome_travis_ci: {
                base: 'ChromeHeadless',
                flags: ['--no-sandbox', '--disable-gpu']
            }
        }
    }

    if (process.env.TRAVIS) {
        configuration.browsers = ['Chrome_travis_ci'];
    }

    config.set(configuration);
}
