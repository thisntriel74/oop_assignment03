# /************************************/
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# /************************************/
# Bài thực hành tuần 3-4: Nạp chồng (overloading) - Nhóm dự án và nhân sự
#
# Lưu ý về Python: KHÔNG hỗ trợ nạp chồng như C#/Java, nên:
#   - Nạp chồng constructor/phương thức  -> dùng tham số mặc định
#   - Constructor thay thế               -> dùng @classmethod
#   - Phương thức "virtual"              -> mọi phương thức Python đều ghi đè được


# ------------------------- Hàm kiểm tra dùng chung -------------------------
def _check_text(value, field_name):
    """Chuỗi phải đúng kiểu str và không rỗng (sau khi bỏ khoảng trắng hai đầu)."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} phải là chuỗi!")
    value = value.strip()
    if value == "":
        raise ValueError(f"{field_name} không được rỗng!")
    return value


def _check_number(value, field_name):
    """Giá trị phải là số (int/float); bool không được chấp nhận."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} phải là số!")
    return float(value)


class Employee:
    """Nhân sự thông thường.

    Trách nhiệm: lưu thông tin cơ bản và tính chi phí hằng tháng.
    Bất biến: mã không rỗng, họ tên không rỗng, lương cơ bản không âm.
    """

    # Nạp chồng constructor bằng tham số mặc định:
    #   Employee()                       -> dùng cả 3 giá trị mặc định
    #   Employee(id, full_name)          -> lương = 0
    #   Employee(id, full_name, salary)  -> đủ 3 tham số
    def __init__(self, emp_id="UNKNOWN", full_name="Unnamed employee", base_salary=0.0):
        # Kiểm tra hết rồi mới gán, để đối tượng lỗi không bị tạo dở dang
        emp_id = _check_text(emp_id, "Mã nhân sự")
        full_name = _check_text(full_name, "Họ tên")
        base_salary = _check_number(base_salary, "Lương cơ bản")
        if base_salary < 0:
            raise ValueError("Lương cơ bản không được âm!")

        # Thuộc tính "private" (dấu _) để bên ngoài không gán trực tiếp làm phá bất biến
        self._id = emp_id
        self._full_name = full_name
        self._base_salary = base_salary

    # Getter
    @property
    def id(self):
        return self._id

    @property
    def full_name(self):
        return self._full_name

    @property
    def base_salary(self):
        return self._base_salary

    # Nạp chồng increaseSalary bằng tham số mặc định:
    #   increase_salary(amount)                -> tăng số tiền cố định
    #   increase_salary(value, by_percentage)  -> True: tăng theo %, False: cố định
    def increase_salary(self, value, by_percentage=False):
        value = _check_number(value, "Giá trị tăng")
        if value <= 0:
            raise ValueError("Giá trị tăng phải dương!")
        if not isinstance(by_percentage, bool):
            raise TypeError("by_percentage phải là True/False!")

        if by_percentage:
            self._base_salary += self._base_salary * (value / 100)
        else:
            self._base_salary += value

    # Mặc định chi phí tháng = lương cơ bản (lớp con có thể ghi đè -> đa hình)
    def calculate_monthly_cost(self):
        return self._base_salary

    def display_info(self):
        print(f"[{self._id}] {self._full_name} | Lương CB: {self._base_salary:,.0f} VNĐ")

    # Destructor: in thông báo để quan sát vòng đời đối tượng
    def __del__(self):
        # Nếu constructor báo lỗi giữa chừng thì đối tượng chưa có _id -> bỏ qua
        if hasattr(self, "_id"):
            print(f"[Hủy] Employee {self._id}")


class SoftwareEngineer(Employee):
    """Kỹ sư phần mềm: kế thừa Employee, thêm ngôn ngữ chính và phụ cấp kỹ thuật.

    Bất biến (thêm so với Employee): ngôn ngữ chính không rỗng, phụ cấp không âm.
    """

    # Constructor 2 của đề: (id, fullName, baseSalary, primaryLanguage, technicalAllowance)
    def __init__(self, emp_id, full_name, base_salary, primary_language, tech_allowance):
        # super() gọi hàm khởi tạo của lớp cha (Employee) để xử lý Mã, Tên, Lương
        super().__init__(emp_id, full_name, base_salary)

        primary_language = _check_text(primary_language, "Ngôn ngữ lập trình chính")
        tech_allowance = _check_number(tech_allowance, "Phụ cấp")
        if tech_allowance < 0:
            raise ValueError("Phụ cấp không được âm!")

        self._primary_language = primary_language
        self._tech_allowance = tech_allowance

    # Constructor 1 của đề: (id, fullName, primaryLanguage)
    # Python không nạp chồng constructor -> dùng classmethod làm constructor thay thế
    @classmethod
    def with_language(cls, emp_id, full_name, primary_language):
        return cls(emp_id, full_name, 0.0, primary_language, 0.0)

    # Getter
    @property
    def primary_language(self):
        return self._primary_language

    @property
    def tech_allowance(self):
        return self._tech_allowance

    # Ghi đè: chi phí tháng = lương cơ bản + phụ cấp
    def calculate_monthly_cost(self):
        return self._base_salary + self._tech_allowance

    # Ghi đè: hiển thị thêm ngôn ngữ và phụ cấp
    def display_info(self):
        print(f"[{self._id}] {self._full_name} (Dev {self._primary_language}) | "
              f"Lương: {self._base_salary:,.0f} | Phụ cấp: {self._tech_allowance:,.0f}")

    def __del__(self):
        if hasattr(self, "_primary_language"):
            print(f"[Hủy] SoftwareEngineer {self._id}")
        # Python KHÔNG tự gọi destructor lớp cha -> gọi tường minh
        super().__del__()


class ProjectTeam:
    """Nhóm dự án - quan hệ KẾT TẬP (aggregation) với Employee.

    Nhóm chỉ giữ THAM CHIẾU tới Employee (không sở hữu): hủy nhóm không hủy nhân sự,
    và một nhân sự có thể thuộc nhiều nhóm.
    Bất biến: trưởng nhóm (nếu có) luôn nằm trong danh sách thành viên;
    không có hai thành viên cùng mã; mã và tên dự án không rỗng.
    """

    # Nạp chồng constructor bằng tham số mặc định:
    #   ProjectTeam(code, name)          -> nhóm chưa có trưởng nhóm
    #   ProjectTeam(code, name, leader)  -> đặt trưởng nhóm, tự đưa vào danh sách
    def __init__(self, project_code, project_name, leader=None):
        self._project_code = _check_text(project_code, "Mã dự án")
        self._project_name = _check_text(project_name, "Tên dự án")

        self._leader = None
        self._members = []

        if leader is not None:
            self.add_member(leader, make_leader=True)

    # Getter
    @property
    def project_code(self):
        return self._project_code

    @property
    def project_name(self):
        return self._project_name

    @property
    def leader(self):
        return self._leader

    @staticmethod
    def _check_employee(employee):
        """Đối số phải là Employee (hoặc lớp con)."""
        if not isinstance(employee, Employee):
            raise TypeError("Tham số phải là đối tượng Employee!")

    # Nạp chồng addMember bằng tham số mặc định:
    #   add_member(employee)                   -> chỉ thêm thành viên
    #   add_member(employee, make_leader=True) -> thêm và đặt làm trưởng nhóm
    # Trả về True nếu thêm được, False nếu bị từ chối (đã có mã này trong nhóm).
    # Trưởng nhóm cũ vẫn là thành viên. Muốn đổi trưởng nhóm cho người đã có: change_leader.
    def add_member(self, employee, make_leader=False):
        self._check_employee(employee)
        if self.contains(employee.id):
            return False

        self._members.append(employee)
        if make_leader:
            self._leader = employee
        return True

    def remove_member(self, employee_id):
        # Không cho xóa trưởng nhóm khi chưa chọn người thay thế
        if self._leader and self._leader.id == employee_id:
            print(f"Từ chối: Không thể xóa trưởng nhóm {employee_id} khi chưa chọn người thay thế.")
            return False

        for i, emp in enumerate(self._members):
            if emp.id == employee_id:
                del self._members[i]
                return True
        return False

    def change_leader(self, employee):
        self._check_employee(employee)
        # Trùng mã nhưng là đối tượng khác -> vi phạm bất biến, từ chối
        for emp in self._members:
            if emp.id == employee.id and emp is not employee:
                print(f"Từ chối: Mã {employee.id} đã tồn tại trong nhóm với nhân sự khác.")
                return False

        # Trưởng nhóm mới phải thuộc nhóm, nếu chưa thì thêm vào
        if not self.contains(employee.id):
            self.add_member(employee)
        self._leader = employee
        return True

    def contains(self, employee_id):
        return any(emp.id == employee_id for emp in self._members)

    def calculate_total_monthly_cost(self):
        # Đa hình: mỗi nhân sự tự tính chi phí theo lớp của mình
        return sum(emp.calculate_monthly_cost() for emp in self._members)

    def display_team(self):
        print(f"\n--- DỰ ÁN: {self._project_code} - {self._project_name} ---")
        if self._leader:
            print(f"Trưởng nhóm: {self._leader.full_name}")
        else:
            print("Trưởng nhóm: Chưa có")

        print(f"Danh sách thành viên ({len(self._members)} người):")
        for emp in self._members:
            emp.display_info()  # Đa hình: gọi đúng display_info() của từng lớp
        print(f"Tổng chi phí dự án: {self.calculate_total_monthly_cost():,.0f} VNĐ")

    # Destructor: chỉ dọn danh sách liên kết nội bộ, KHÔNG hủy các Employee
    def __del__(self):
        if hasattr(self, "_members"):
            print(f"[Hủy] ProjectTeam {self._project_code}")
            self._members.clear()
            self._leader = None


# ------------------------------ Hàm phụ cho phần test ------------------------------
def expect_error(label, func):
    """Chạy func và mong đợi báo lỗi, để chứng minh ràng buộc hoạt động."""
    try:
        func()
        print(f"[SAI] {label}: lẽ ra phải báo lỗi")
    except (ValueError, TypeError) as e:
        print(f"[OK] {label} -> bị từ chối: {e}")


def tao_va_huy_nhom_2(employee):
    """Bước 13-14: nhóm 2 chỉ sống trong hàm này (thay cho khối lệnh cục bộ)."""
    print("\n[THAO TÁC] Tạo nhóm 2 và thêm nhân sự đã có ở nhóm 1:")
    team2 = ProjectTeam("P02", "App B")
    print("Thêm nhân sự vào nhóm 2:", team2.add_member(employee))
    team2.display_team()
    print("\n[THAO TÁC] Kết thúc hàm -> nhóm 2 tự bị hủy:")
    # Hết hàm, team2 ra khỏi phạm vi nên Python tự hủy nhóm 2


if __name__ == "__main__":
    # --- KIỂM THỬ KỊCH BẢN ---

    # 1. Tạo hai Employee bằng hai constructor khác nhau
    emp1 = Employee("NV01", "Pham Van Z")
    emp2 = Employee("NV02", "Nguyen Van A", 10000000)

    # 2. Tạo hai SoftwareEngineer bằng hai constructor khác nhau
    dev1 = SoftwareEngineer.with_language("DEV01", "Tran Van B", "C++")
    dev2 = SoftwareEngineer("DEV02", "Le Thi C", 20000000, "Python", 5000000)

    # 3. Tăng lương một nhân sự bằng tiền cố định
    emp2.increase_salary(2000000)

    # 4. Tăng lương một nhân sự khác theo phần trăm
    dev2.increase_salary(10, by_percentage=True)

    # 5. Tạo nhóm dự án không có leader
    team1 = ProjectTeam("P01", "Website A")

    # 6. Thêm một nhân sự vào bằng addMember
    print("\n[THAO TÁC] Thêm emp2 vào nhóm:", team1.add_member(emp2))

    # 7. Thêm một kĩ sư để đặt làm leader
    print("[THAO TÁC] Thêm dev1 làm trưởng nhóm:", team1.add_member(dev1, make_leader=True))

    # 8. Thử thêm lại một thành viên đã tồn tại
    print("[THAO TÁC] Thêm lại emp2 (đã tồn tại):", team1.add_member(emp2))

    # 9. Hiển thị danh sách đa hình
    team1.display_team()

    # 10. Tính tổng chi phí nhân sự hằng tháng
    print(f"\n[KẾT QUẢ] Tổng chi phí nhân sự hằng tháng: {team1.calculate_total_monthly_cost():,.0f} VNĐ")

    # 11. Thử xóa trưởng nhóm hiện tại -> phải bị từ chối
    print("\n[THAO TÁC] Thử xóa trưởng nhóm hiện tại (DEV01):")
    print("Kết quả xóa:", team1.remove_member("DEV01"))

    # 12. Đổi trưởng nhóm sang DEV02 rồi xóa trưởng nhóm cũ DEV01
    print("\n[THAO TÁC] Đổi trưởng nhóm sang DEV02 (chưa là thành viên):", team1.change_leader(dev2))
    print("[THAO TÁC] Xóa DEV01:", team1.remove_member("DEV01"))
    team1.display_team()

    # 13-14. Tạo nhóm thứ hai, thêm nhân sự đã có ở nhóm 1, rồi hủy nhóm 2 khi hết hàm
    tao_va_huy_nhom_2(emp2)

    # 15. Chứng minh nhân sự của nhóm thứ hai vẫn tồn tại sau khi hủy nhóm
    print("\n[KẾT QUẢ] Kiểm tra sự tồn tại của nhân sự NV02 sau khi nhóm 2 bị hủy:")
    emp2.display_info()
    print("NV02 vẫn thuộc nhóm 1:", team1.contains("NV02"))

    # --- CÁC TRƯỜNG HỢP BIÊN ---
    print("\n========== CÁC TRƯỜNG HỢP BIÊN ==========")
    emp_default = Employee()  # dùng toàn bộ giá trị mặc định
    emp_default.display_info()
    expect_error("Mã rỗng", lambda: Employee("", "X"))
    expect_error("Họ tên toàn khoảng trắng", lambda: Employee("NV09", "   "))
    expect_error("Lương âm", lambda: Employee("NV09", "X", -1))
    expect_error("Ngôn ngữ chính rỗng", lambda: SoftwareEngineer.with_language("DEV09", "X", ""))
    expect_error("Phụ cấp âm", lambda: SoftwareEngineer("DEV09", "X", 1000, "Java", -5))
    expect_error("Tăng lương bằng 0", lambda: emp2.increase_salary(0))
    expect_error("Tăng lương âm theo %", lambda: emp2.increase_salary(-5, True))
    expect_error("Thêm None vào nhóm", lambda: team1.add_member(None))
    print("Xóa mã không tồn tại:", team1.remove_member("KHONG_CO"))
    emp_trung = Employee("NV02", "Nguoi trung ma")
    print("Thêm người khác nhưng trùng mã NV02:", team1.add_member(emp_trung))
    print("Đặt người trùng mã làm trưởng nhóm:", team1.change_leader(emp_trung))

    print("\n========== KẾT THÚC CHƯƠNG TRÌNH ==========")