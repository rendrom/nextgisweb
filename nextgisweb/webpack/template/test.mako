<%inherit file='nextgisweb:templates/base.mako' />

<button id="testDijit">Test dijit</button>
<button id="testLodash">Test lodash</button>

<script>
    require(["dojo/domReady!"], function () {
        document.getElementById("testDijit").onclick = function () {
            require(['@nextgisweb/webpack'], function (module) {
                module.testDijit();
            })
        };
        document.getElementById("testLodash").onclick = function () {
            require(['@nextgisweb/webpack'], function (module) {
                module.testLodash();
            })
        };
    })
</script>