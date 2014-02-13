#-------------------------------------------------------------------------------
# Name:        tasks
# Purpose:     entry point for task-related tasks
#
# Author:      Eric
#
# Created:     13/02/2014
# Copyright:   (c) Eric 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import webapp2
import taskhandlers
import config
import routes
webapp2_config = config.config

app = webapp2.WSGIApplication(debug=True, config=webapp2_config)
routes.add_routes(app)

