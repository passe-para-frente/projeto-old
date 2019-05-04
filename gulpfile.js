const gulp = require('gulp');
const concat = require('gulp-concat');
const cleanCSS = require('gulp-clean-css');
const webpack = require('webpack');
const webpackStream = require('webpack-stream');
const webpackConfig = require('./webpack.config.js');

gulp.task('django', function () {
    const spawn = require('child_process').spawn;
    return spawn('python', ['manage.py', 'runserver'])
        .stderr.on('data', (data) => {});
});

gulp.task('watch', function () {
    gulp.watch(['landing/static/css/*.css'], ['minify-css']);
    gulp.watch(['landing/static/js/*.js'], ['pack-js']);
});

gulp.task('minify-css', function () {
    return gulp.src(['landing/static/css/*.css'])
        .pipe(concat('main.min.css'))
        .pipe(cleanCSS())
        .pipe(gulp.dest('passe_pra_frente/static/css'));
});

gulp.task('pack-js', function () {
  return gulp.src('./landing/static/js/init.js')
    .pipe(webpackStream(webpackConfig), webpack)
    .pipe(gulp.dest('./passe_pra_frente/static/js/'));
});

gulp.task('default',
    [
        'django',
        'minify-css',
        'pack-js',
        'watch'
    ]
);

gulp.task('build',
    [
        'minify-css',
        'pack-js'
    ]
);
