// Take type and make it lowercase, single word.
module.exports = function (migration) {
    const show = migration.editContentType('show')
    migration.transformEntries({
        contentType:'show',
        from: ['type'],
        to: ['type'],
        transformEntryForLocale: function (fromFields, currentLocale) {
            var modifiedType = [`${fromFields.type[currentLocale]}`.replace(/\s+/g, '')];
            console.log(modifiedType);
            return { type: modifiedType };
        }
    });
}
