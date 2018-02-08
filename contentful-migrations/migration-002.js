// Take last word in title and use it to create a slug.
module.exports = function (migration) {
    const show = migration.editContentType('show')
    show
        .createField('slug')
        .name('slug')
        .type('Symbol')
        .required(true)
        .validations([{"unique": true}]);
    migration.transformEntries({
        contentType:'show',
        from: ['title'],
        to: ['slug'],
        transformEntryForLocale: function (fromFields, currentLocale) {
            if (currentLocale === 'de-DE') {
                return;
            }
            var newSlug = `${fromFields.title[currentLocale]}`.split(" ");
            newSlug = newSlug[newSlug.length - 1].toLowerCase()
            console.log(newSlug);
            return { slug: newSlug };
        }
    });
}
