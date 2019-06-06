######################
Platform Sections
######################

Platform Sections allows for showing or hiding content sections based on which platform the documentation is being built for.

A platform section is delimited by ``@![platform,section]`` and ``!@``. Section names are case insensitive and multiple
platform sections can be comma separated in the tag as shown above.

The configuration for the platform section is just ``platform_section`` as shown below. This is the section that will be
shown for that build and other sections will be hidden.

==============
Configuration
==============

``platform_section``
    Case insensitive name of section to show. All other sections will be hidden.

=======
Usage
=======
In documents
-------------

.. code-block:: html

   @![Android]
   This section will be shown for the Android build
   !@

   @![iOS]
   This section will be displayed for the iOs build.
   !@

   @![JavaSE,JavaEE]
   This section will be displayed for Java SE and EE builds.
   !@

Inline platform section tags are also supported:

.. code-block:: html5

   ### 1. Creating an App Service Manifest
   The first step to publishing is to create an @![iOS]`SDLAppServiceManifest`!@ @![Android, JavaSE, JavaEE]`AppServiceManifest`!@ object.

Python
--------------

.. code-block:: python

    config = {
        'docdown.platform_section': {
            'platform_section': 'Android',
        },
    }

    text = ('@![iOS]\n'
            'some iOS content not shown\n\n'
            '!@\n'
            '\n'
            '@![Android]\n'
            'some Android content shown\n\n'
            '!@\n')

    html = markdown.markdown(
            text,
            extensions=['docdown.platform_section'],
            extension_configs=config,
            output_format='html5')

=======
Output
=======

.. code-block:: html

   <p>some Android content shown</p>
