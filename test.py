from abc import ABC, abstractmethod
from datetime import datetime
import locale
from enum import Enum
locale.setlocale(locale.LC_ALL, 'vi_VN.utf-8')

#super class
class Motorbike(ABC):
    _exists_ids = set()

    def __init__(self, id, name, import_date, price):
        if not id:
            raise ValueError("Mã xe không được để trống!")
        if id in Motorbike._exists_ids:
            raise ValueError(f"ID này '{id}' đã tồn tại!")
        self._id = id
        Motorbike._exists_ids.add(id)
        print(f"Thêm thành công '{id}'")
        self.name = name
        self.import_date = import_date
        self.price = price

    @property
    def  id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError('Chưa nhập tên')
        self._name = value

    @property
    def import_date(self):
        return self._import_date
    
    @import_date.setter
    def import_date(self, date):
        if not date:
            raise ValueError('Vui lòng nhập ngày nhập kho')
        try: 
            dt_date = datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            raise ValueError('Ngày phải tuân thủ định dạng dd/mm/yyyy')
        self._import_date = dt_date
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if isinstance(value, str):
            new_value = value.replace('.','').replace(',','').strip()
            if not new_value.isdigit():
                raise ValueError('Giá phải là chữ số')
            value = int(new_value)
        if value <= 0:
            raise ValueError('Giá phải lớn hơn 0')
        self._price = value

    @abstractmethod
    def tax(self):
        pass

    @abstractmethod
    def total_price(self):
        pass

    def __str__(self):
        date_str = self.import_date.strftime('%d/%m/%Y')
        price_str = locale.currency(self.price, grouping=True)
        return f"{self.id:^6}|{self.name:>10}|{date_str:<10}|{price_str:^12}"
    
#subclass (Domestic Motorbike)
class Company(Enum):
    HONDA = 'Honda'
    SUZUKI = 'Suzuki'
    SYM = 'SYM'

class Domestic(Motorbike): 
    
    def __init__(self, id, name, import_date, price, manufacturer: Company):
        super().__init__(id, name, import_date, price)
        self.manufacturer = manufacturer
        
    @property
    def manufacturer(self):
        return self._manufacturer
    
    @manufacturer.setter
    def manufacturer(self, value):
        self._manufacturer = ('No value' if not value else value)

    def tax(self):
        if self.manufacturer == Company.HONDA:
            return self.price * 0.1
        else:
            return self.price * 0.15
        
    def total_price(self):
        return self.price + self.tax() + (100000 if self.import_date < datetime(2024,1,1) else 0)
    
    def __str__(self):
        base_str = super().__str__()
        price_fm = locale.currency(self.total_price(), grouping=True)
        return f"|{base_str:38}|{self.manufacturer.value if hasattr(self.manufacturer,'value') else self.manufacturer:6}|{'':7}|{price_fm:>15}|"

#subclass (Foreign Motorbike)
class Country(Enum):
    ASEAN = 'ASEAN'
    EUROPE = 'Europe'
    USA = 'USA'

class Foreign(Motorbike):
    
    def __init__(self, id, name, import_date, price, country: Country, company):
        super().__init__(id, name, import_date, price)
        self.country = country
        self.company = company

    @property
    def country(self):
        return self._country
    
    @country.setter
    def country(self, value):
        self._country = value

    @property
    def company(self):
        return self._company

    @company.setter
    def company(self, value):
        if not value:
            raise ValueError('Vui lòng nhập tên công ty')
        self._company = value

    def tax(self):
        return self.price * (0.15 if self.country == Country.ASEAN else 0.2)
    
    def total_price(self):
        return self.price + self.tax()

    def __str__(self):
        base_str = super().__str__()
        price_fm = locale.currency(self.total_price(), grouping=True)
        return f"|{base_str:38}|{self.country.value if hasattr(self.country, 'value') else self.country:6}|{self.company:^7}|{price_fm:>15}|"

#Interface
class Task(ABC):

    @abstractmethod
    def add(self, moto): #add
        pass

    @abstractmethod
    def sreach(self, id): #find by id
        pass
    
    @abstractmethod
    def print_all(self): #show
        pass

    @abstractmethod
    def sort(self): #sort
        pass

    @abstractmethod
    def statistic(self): # ?domesstic & ?foreign
        pass

#Management
class Management(Task):

    def __init__(self):
        self.ds = []

    def add(self, moto):
        self.ds.append(moto)

    def sreach(self, id):
        for xe in self.ds:
            if xe.id == id:
                return xe        
        return None
    
    def sort(self):
        sorted_ds = sorted(self.ds, key=lambda x: (x.price, -x.import_date.timestamp()))
        for xe in sorted_ds:
            print(xe)

    def statistic(self):
        noi = sum(isinstance(x, Domestic) for x in self.ds)
        nhap = sum(isinstance(x, Foreign) for x in self.ds)
        print(f"\nTồn kho: {noi} xe Nội & {nhap} xe Nhập.\n")

    def print_all(self):
        for xe in self.ds:
            print(xe)

class Test:

    def main():
        xe_1 = Domestic('xn1', 'RSX', '12/12/2020', '2.000', Company.HONDA)
        xe_2 = Domestic('xn2', 'an', '11/09/2019', '23,456', Company.SUZUKI)
        xe_3 = Domestic('xn3', 'bin', '24/12/2023', '2.0000', Company.SYM)
        xe_4 = Foreign('xnh7', 'pnlh', '06/07/2024', '234,56', Country.EUROPE, 'BMW')
        xe_5 = Foreign('xnh8', 'pnha', '01/01/2022', '234,56', Country.USA, 'Ford')
        xe_6 = Foreign('xnh9', 'ntpanh', '06/02/2024', '25556', Country.ASEAN, 'Audi')

        ql = Management()

        ql.add(xe_1)
        ql.add(xe_2)
        ql.add(xe_3)
        ql.add(xe_4)
        ql.add(xe_5)
        ql.add(xe_6)
        print("\n\n")
        ###############################
        while True:
            print('~'*100)
            print('~'*100,'\n')
            print("\n===== QUẢN LÝ XE MÁY =====")
            print("1. Hiển thị tất cả")
            print("2. Tìm xe theo ID")
            print("3. Sắp xếp theo giá")
            print("4. Thống kê số lượng")
            print("5. Thoát")
            
            choice = input("Chọn: ").strip()

            match choice:
                case "1":
                    #header
                    print('~'*74)
                    print(f"|{'ID':^6}|{'Name':^10}|{'Entry Date':^10}|{'Price':^12}|{'Note':^6}|{'Company':^7}|{'Total Cost':^15}|")
                    print('~'*74)
                    ########
                    ql.print_all()
                
                case "2":
                    id = str(input('Nhập id: ')).strip()
                    xe = ql.sreach(id)
                    if xe:
                        #header
                        print('~'*74)
                        print(f"|{'ID':^6}|{'Name':^10}|{'Entry Date':^10}|{'Price':^12}|{'Note':^6}|{'Company':^7}|{'Total Cost':^15}|")
                        print('~'*74)
                        ########
                        print(xe)
                    else:
                        print('Không có kết quả')
                
                case "3":
                    print("Danh sách sau khi đã sắp xếp:\n")
                    #header
                    print('~'*74)
                    print(f"|{'ID':^6}|{'Name':^10}|{'Entry Date':^10}|{'Price':^12}|{'Note':^6}|{'Company':^7}|{'Total Cost':^15}|")
                    print('~'*74)
                    ########
                    ql.sort()

                case "4":
                    print('Thống kê sản phẩm:\n')
                    ql.statistic()

                case "5":
                    print('Đã thoát chương trình!')
                    break

                case _:
                    print('Lựa chọn không hợp lệ!')
            print('\n\n')

if __name__ == '__main__':
    Test.main()