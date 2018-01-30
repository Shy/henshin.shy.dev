// Create character content model and update show update model to contain list of characters.
module.exports = function (migration) {
    const character = migration.createContentType('character')
        .name('Character')
        .description('Character of a show')
    character
        .createField('full_name')
        .name('Full name')
        .type('Symbol')
        .required(true)
    character
        .createField('job_title')
        .name('Job name')
        .type('Symbol')
        .required(true)
    character
        .createField('untransformed_photo')
        .name('untransformed_photo')
        .type('Link')
        .linkType('Asset')
        .required(true)
    character
        .createField('transformed_photo')
        .name('transformed_photo')
        .type('Link')
        .linkType('Asset')
        .required(true)
};
