import unittest

from dobbyt.validators import LocationsValidator, ValidationFailed


z = (0, 0, 0)
w = (255, 255, 255)

testimage = [
    [z, z, z, z, z],
    [z, w, w, w, w],
    [z, w, w, w, w],
    [z, w, w, w, w],
    [z, z, z, z, z],
]

class LocationsValidatorTests(unittest.TestCase):

    #------------------------------------------------------------
    def test_set_properties(self):
        val = LocationsValidator(testimage)
        val.default_valid = True
        val.valid_colors = w
        val.valid_colors = [w, z]
        val.valid_colors = (w, z)
        val.valid_colors = {w, z}
        val.invalid_colors = w
        val.invalid_colors = [w, z]
        val.invalid_colors = (w, z)
        val.invalid_colors = {w, z}


    #------------------------------------------------------------
    def test_set_bad_colors(self):
        val = LocationsValidator(testimage)

        try:
            val.valid_colors = 3
            self.fail()
        except:
            pass

        try:
            val.valid_colors = (1,2)
            self.fail()
        except:
            pass

        try:
            val.valid_colors = (0,0,256)
            self.fail()
        except:
            pass

        try:
            val.valid_colors = (0,-1,255)
            self.fail()
        except:
            pass


    #------------------------------------------------------------
    def test_set_bad_default(self):
        val = LocationsValidator(testimage)

        try:
            val.default_valid = None
            self.fail()
        except:
            pass

        try:
            val.default_valid = ""
            self.fail()
        except:
            pass


    #------------------------------------------------------------
    def test_validate_default_invalid(self):
        val = LocationsValidator(testimage, enabled=True)
        val.valid_colors = w

        self.assertRaises(ValidationFailed, lambda:val.mouse_at(0, -2))
        self.assertRaises(ValidationFailed, lambda:val.mouse_at(0,  2))
        self.assertRaises(ValidationFailed, lambda:val.mouse_at(-2, 0))
        val.mouse_at(2, 0)
        self.assertRaises(ValidationFailed, lambda:val.mouse_at(10, 10))  # out of image


    #------------------------------------------------------------
    def test_validate_default_valid(self):
        val = LocationsValidator(testimage, default_valid=True, enabled=True)
        val.invalid_colors = z

        self.assertRaises(ValidationFailed, lambda:val.mouse_at(0, -2))
        self.assertRaises(ValidationFailed, lambda:val.mouse_at(0, 2))
        self.assertRaises(ValidationFailed, lambda:val.mouse_at(-2, 0))
        val.mouse_at(2, 0)
        val.mouse_at(10, 10) # out of image

    #------------------------------------------------------------
    def test_disabled(self):
        val = LocationsValidator(testimage)
        val.valid_colors = w
        val.mouse_at(0, -2)


if __name__ == '__main__':
    unittest.main()
