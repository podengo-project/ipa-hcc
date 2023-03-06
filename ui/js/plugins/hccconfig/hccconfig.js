//
// IPA plugin for Hybrid Cloud Console
// Copyright (C) 2022  Christian Heimes <cheimes@redhat.com>
// See COPYING for license
//

define([
    'freeipa/phases',
    'freeipa/ipa'
],
function(phases, IPA) {

    // helper function
    function get_item(array, attr, value) {
        for (var i = 0, l = array.length; i < l; i++) {
            if (array[i][attr] === value) return array[i];
        }
        return null;
    }

    var hcc_config_plugin = {};

    hcc_config_plugin.add_hcc_config_pre_op = function() {
        var section = {
            name: 'hcc',
            label: '@i18n:hccconfig.name',
            fields: [{
                name: 'hccorgid',
                flags: ['w_if_no_aci']
            }]
        };
        var facet = get_item(IPA.serverconfig.entity_spec.facets, '$type', 'details');
        facet.sections.push(section);

        var field = {
            $type: 'multivalued',
            name: 'hcc_enrollment_server_server',
            read_only: true
        };
        var server_section = get_item(facet.sections, 'name', 'server');
        server_section.fields.push(field);

        return true;
    };

    phases.on('customization', hcc_config_plugin.add_hcc_config_pre_op);

    return hcc_config_plugin;
});
