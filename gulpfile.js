var gulp = require('gulp');
var autoprefixer = require('gulp-autoprefixer');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var debug = require('gulp-debug');
var fs = require('fs');
var shell = require('gulp-shell');

var concat = require('gulp-concat');
var notify = require('gulp-notify');
var notifier = require('node-notifier');
var cache = require('gulp-cache');

var docsfiles = ['docs/*.rst'];

var rstfiles = ['docs/*.rst', 'docs/dev/*.rst', 'docs/js/ubl-tebl.js', 'docs/css/ubl-tebl.css'];
var pyfiles = ['src/ubl/tebl/*.py', 'src/ubl/tebl/browser/*.py', 'docs/conf.py'];
var documentation_files = pyfiles.concat(rstfiles)

var readme = 'README.rst'
w = process.cwd();

var gulp = require('gulp')
var shell = require('gulp-shell')

gulp.task('notifing', ['build-docs'], function() {
    notifier.notify({title: 'Sphinx',
              message: 'build finished...'
    })
});


gulp.task('build-docs', shell.task('bin/sphinx-build docs docs/html', {cwd: '.'}))

gulp.task('readme', shell.task('cp README.rst docs', {cwd: '.'}))

gulp.task('docs', ['build-docs'], function() {
  gulp.watch(readme, ['readme'])
  gulp.watch(['./docs/*.rst', './docs/*.py'], ['build-docs'])
})

gulp.task('htmldoc', ['build-docs'], function() {
  gulp.watch(readme, ['readme'])
  gulp.watch(['./docs/*.rst', './docs/*.py'], ['build-docs'])
})

gulp.task('html', function() {
    gulp.watch(documentation_files, ['notifing'])
});


gulp.task('default', ['html']);

/*

docs = gulp.task(
    'docs',
    function() {
        return gulp.src(docsfiles)
        .pipe(shell(['bin/sphinx-build -W docs docs/html']))
        .pipe(notify({message: 'Styles task complete'}))
    });

gulp.task('default', ['styles']);
gulp.task('watch', function() {
  gulp.watch(docsfiles, ['docs']);
});
*/
/* vim:set ft=javascript : */
