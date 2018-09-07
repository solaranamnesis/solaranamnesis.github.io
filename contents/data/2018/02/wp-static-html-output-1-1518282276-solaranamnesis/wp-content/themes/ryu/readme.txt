== Changelog ==

= 8 June 2017 =
* Add title-tag theme support. Fix translation funcion. Bump version number.
* Adding fixes for lists, too long text strings in text widget. Bump version number.

= 7 June 2017 =
* Update JavaScript that toggles hidden widget area, to make sure new video and audio widgets are displaying correctly when opened.

= 5 May 2017 =
* Check for post parent object before outputting post parent information to prevent fatals.

= 28 April 2017 =
* Reduce priority and check first before loading the Tonesque library.

= 18 April 2017 =
* Check for post parent before outputting next, previous, and image attachment information to prevent fatals.

= 22 March 2017 =
* add Custom Colors annotations directly to the theme
* move fonts annotations directly into the theme

= 9 February 2017 =
* Check for is_wp_error() in cases when using get_the_tag_list() to avoid potential fatal errors.

= 17 June 2016 =
* Add a class of .widgets-hidden to the body tag when the sidebar is active; allows the widgets to be targeted by Direct Manipulation.

= 27 May 2016 =
* fix the behavior of `*_the_attached_image()` for PHP 7 compat

= 13 January 2016 =
* spell GitHub correctly.

= 18 December 2015 =
* Allow users to restore default gravatar header image.

= 27 October 2015 =
* Add an Instagram link theme option.

= 20 August 2015 =
* Add text domain and/or remove domain path. (O-S)

= 31 July 2015 =
* Remove .`screen-reader-text:hover` and `.screen-reader-text:active` style rules.

= 15 July 2015 =
* Always use https when loading Google Fonts.

= 15 June 2015 =
* Updating version number for regenerated download

= 6 May 2015 =
* Fully remove example.html from Genericons folders.
* Remove index.html file from Genericions.

= 3 March 2015 =
* Allow Tonesque to calculate contrast and add color to Image format posts for oEmbed images (Flickr, for example) by first applying filters to the content before passing it to the regex function. Props @kathrynwp for providing the fix!

= 29 November 2014 =
* Remove unnecessary function for the eventbrite_meta_separator hook.

= 26 November 2014 =
* Ensure Eventbrite templates in themes are not selectable as custom page templates.

= 25 November 2014 =
* Add support for upcoming Eventbrite services.

= 16 September 2014 =
* Add latin extended subset to Google Font Lato.

= 24 July 2014 =
* change theme/author URIs and footer links to `wordpress.com/themes`.

= 9 July 2014 =
* Return early if Tonesque is not available to avoid a fatal error in case it's not available.

= 4 July 2014 =
* prevent fatal errors when sidebar.php tries to call a function that doesn't exist.

= 30 June 2014 =
* Improve form elements' style

= 10 June 2014 =
* Update POT version.
* Set a sanitization callback for the Gravatar email setting.

= 1 June 2014 =
* add/update pot files.

= 21 February 2014 =
* Update Genericons to 3.0.3 and enqueue its own stylesheet.

= 18 February 2014 =
* Making sure sharing buttons on image format align same as text.

= 17 February 2014 =
* Remove a border from sharedaddy containers.

= 5 February 2014 =
* Replace .genericon class with updated .theme-genericon so the Aside icon will appear for logged out users.
* Replace esc_url with esc_url_raw and sanitize_email with is_email, props @kobenland.
* Ensure link values are sanitized before entering the database.

= 26 January 2014 =
* Use the post_id passed to the action - the global is not always available.

= 24 January 2014 =
* Rename the .genericon class to .theme-genericon to avoid conflict with other uses of the class name outside of the theme.

= 6 December 2013 =
* Add gravatar theme option to allow users to use a different email address instead of the admin email address.
* update Width terms to Layout.

= 29 November 2013 =
* Remove wildcard navigation selector to avoid accidental matches with user content.

= 6 November 2013 =
* Update changelog
* Update version number

= 16 September 2013 =
* update bundled Jetpack_Color lib to check for the proper class everywhere.

= 13 September 2013 =
* namespace color manipulation library previously called simply `Color` as the name is too generic.

= 11 September 2013 =
* Cache Tonesque values.
* Update Genericons to 2.09.

= 10 September 2013 =
* update bundled Tonesque and Color libs; load them from the wpcom library if possible

= 5 August 2013 =
* update author in footer and stylesheet.

= 26 July 2013 =
* Missing closing quote in Quote post format causes broken links.

= 25 July 2013 =
* Update function_exists check around ryu_entry_meta to reference the proper function (ryu_entry_meta instead of ryu_posted_on)

= 24 July 2013 =
* remove hardcoded inclusion of wpcom.php.

= 22 July 2013 =
* Let core handle show/hide of text with custom header image.
* Move to a custom template tag to display the image and streamline template logic and markup.
* Re-organize file includes to the bottom of the file for consistency.
* Clean up content templates and remove redundant title attributes.
* Revert tonesque changes.
* Use term description rather than taxonomy-specific descriptions.

= 19 July 2013 =
* temporarily remove require_lib( 'tonesque' ), since it's causing errors and breaking image posts.
* Revert r14650 as the underlying cause of the fatal error was dealt with.
* Tonesque library

= 18 July 2013 =
* Change how Tonesque library is loaded.

= 10 July 2013 =
* Move away from using deprecated functions and improve compliance with .org theme review guidelines.

= 13 May 2013 =
* Update license.

= 8 May 2013 =
* Typo in the description -- an extra 'a'

= 7 May 2013 =
* Make sure the private var $color exists inside the Tonesque instance before attempting to get a maxcontrast value from it. This prevents a fatal error when the processed file is not gif, png, jpg, or jpeg. props @matiasventura.

= 2 May 2013 =
* Add forward compat with 3.6.
* Make sure `$first_image` returns the image url correctly when an image posted with the new post format UI. Props @kobenland

= 26 April 2013 =
* Minor coding style

= 24 April 2013 =
* Tweak the slideshow style to match with the theme.
* Reset teh default padding for VideoPress in the theme.
* Revert the last change and display a post thumbnail on pages too.
* Featured image fix for pages.

= 22 April 2013 =
* Minor coding style
* Don't bother specifying WP defaults for the Customizer.

= 19 April 2013 =
* Cleaner code for dequeuing the Google Fonts. Props @kobenland

= 18 April 2013 =
* Cleaner way to check if social links need be displayed.

= 12 April 2013 =
* update `TypekitData` upgrade checks to use `CustomDesign::is_upgrade_active()` instead.

= 11 April 2013 =
* Move the style adjustments for the contact form out from WP.com specific section to Jetpack section.
* Change the release date in readme.txt for .org submission.
* Update the POT file.

= 10 April 2013 =
* Custom Header
* Remove all @since DocBlocks.
* Use imagecolorsforindex for creating the colors in rgb values to avoid issues with gif images. Props @matiasventura.

= 5 April 2013 =
* Slight adjustment for submit buttons in a form.
* Use relative spacing and positioning for the navigation items  so that the dropdown works well  with Custom Fonts.
* Move the stats image little so that it doesn't touch the bottom of the screen.

= 4 April 2013 =
* Update copyright/license notice in the style sheet.
* Make sure the rating doesn't appear in the excerpt in image and gallery formatted post because in these formats, `the_content` and `the_excerpt` can exist together at the same time.
* Style Tweaks

= 3 April 2013 =
* Add a copyright notice in the style sheet.
* Minor style
* Namespacing the theme defined post thumbnail size.

= 2 April 2013 =
* Update the POT file and the screenshot.
* RTL fix.
* Preps for .org submission.
* Style
* Comment out -webkit-calc property value, as this was causing Safari to crash any time post/page navigation is displayed.

= 29 March 2013 =
* Make sure the ellipsis for overflow in post navigation starts right before the arrow.
* Make sure widget areas clear float depending on the size of screen to maintian the grid layout.

= 28 March 2013 =
* Add better screenshot.
* Dim the color of texts in widgets so that links stand out. Also remove border-bottom from link in a list item it's too many lines.
* Add style to links in the Twitter widget and RSS widget.
* Add style to links in the text widget.
* Make the entry title and the category links wider for larger screens.
* Minor style

= 27 March 2013 =
* Make sure the image attachment page show full width image.
* Namespacing the handles for the theme specific js files.
* Make sure Tonesque works in PHP 5.2 also.
* Code style clean up.
* Namesapcing the stylesheet handle.
* Add .pot file for self hosted users.
* Add a screenshot and description of the theme.
* Make sure the calendar widget clears float to maintain the grid layout.
* Add a Post Format Archives heading to archive.php.
* Add title attributes to the triggers because they are only icons.
* Add top margin to the follow button in the Twitter widget.
* Add styles for RTL languages.

= 26 March 2013 =
* Saving spaces in comments area for small screens.
* Code clean up in the JS file and minor style tweak.
* Prevent Tonesque to be conflicted with Custom Colors. Style
* i18n for the category widget title in 404 page.
* Remove settings from the control component because the value is the same as the control component's ID which is the default value of the settings.
* Comment style tweak.
* Adjusting max iwdth for each gallery column setting.
* Style tweak for page links.
* 404 page. Replace the core tag cloud widget with the calendar widget because it doesn't work here WP.com.

= 25 March 2013 =
* Style
* Add comments describing the purpose/use of these functions in the .js file. Also make sure the height of the band would be correct if the post is loaded by IS.
* Fix a typo in the theme tags
* Remove the text link for standard format. It's redundant and it shouldn't be there for the formats Ryu doesn't support such as chat, status, and audio.
* Include WP.com specific functions.
* Make sure if an image is in an image format post before run Tonesque.
* Fix responsive style for video format.
* Style
* Adjustment Tonesque style.
* Enqueue `navigation.js` only when a custom menu is set because Ryu doesn't show a navigation as default. Also some style tweaks.
* Implement Infinite Scroll and style

= 24 March 2013 =
* Styling fix
* Initial import
