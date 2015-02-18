// custom sort functions see http://www.datatables.net/release-datatables/examples/basic_init/multi_col_sort.html
jQuery.fn.dataTableExt.oSort['string-case-asc'] = function (x, y) {
    return ((x < y) ? -1 : ((x > y) ? 1 : 0));
};

jQuery.fn.dataTableExt.oSort['string-case-desc'] = function (x, y) {
    return ((x < y) ? 1 : ((x > y) ? -1 : 0));
};

/* new sort on L1 */
jQuery.fn.dataTableExt.oSort['string-L1-asc'] = function (x, y) {
    var xwords = x.split(' ');
    var ywords = y.split(' ');
    return ((xwords[xwords.length - 1].toLowerCase() < ywords[ywords.length - 1].toLowerCase()) ? -1 : ((xwords[xwords.length - 1].toLowerCase() > ywords[ywords.length - 1].toLowerCase()) ? 1 : 0));
};

jQuery.fn.dataTableExt.oSort['string-L1-desc'] = function (x, y) {
    var xwords = x.split(' ');
    var ywords = y.split(' ');
    return ((xwords[xwords.length - 1].toLowerCase() < ywords[ywords.length - 1].toLowerCase()) ? 1 : ((xwords[xwords.length - 1].toLowerCase() > ywords[ywords.length - 1].toLowerCase()) ? -1 : 0));
};

/* new sort on R1 */
jQuery.fn.dataTableExt.oSort['string-R1-asc'] = function (x, y) {
    var xwords = x.split(' ');
    var ywords = y.split(' ');
    return ((xwords[0].toLowerCase() < ywords[0].toLowerCase()) ? -1 : ((xwords[0].toLowerCase() > ywords[0].toLowerCase()) ? 1 : 0));
};

jQuery.fn.dataTableExt.oSort['string-R1-desc'] = function (x, y) {
    var xwords = x.split(' ');
    var ywords = y.split(' ');
    return ((xwords[0].toLowerCase() < ywords[0].toLowerCase()) ? 1 : ((xwords[0].toLowerCase() > ywords[0].toLowerCase()) ? -1 : 0));
};