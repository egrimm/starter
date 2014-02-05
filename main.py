#-------------------------------------------------------------------------------
# Name:        main
# Purpose:
#
# Author:      egrimm
#
# Created:     16/01/2014
# Copyright:   (c) egrimm 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import webapp2
import handlers
import config
import routes
webapp2_config = config.config

app = webapp2.WSGIApplication(debug=True, config=webapp2_config)
routes.add_routes(app)