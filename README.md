# MongoDB user handler blueprint for Flask

Demo `Flask` application showing how to use the [`user-blueprint`](https://github.com/volfpeter/user-blueprint) project to set up a MongoDB-based user handling web application.

Note that you will need a MongoDB instance to connect to in order to run this demo web application. If you don't your own database, sign up to a service that provides free demo MongoDB databases, such as mLab (mlab.com).

## Dependencies and configuration

The project's dependencies are `pymongo` and `user-blueprint`, both of which can be installed using `pip`.

If you have all dependencies in place, you will only have to configure how your MongoDB database can be accessed. To do this, go to the `Database configuration` section in `mongo_user_bluepring/app.py`.

## How to use

When you are ready with all the above stuff, you may start the `Flask` dev server by running the included `run.py` script.

## License - MIT

The project is open-sourced under the conditions of the MIT [license](https://choosealicense.com/licenses/mit/).
